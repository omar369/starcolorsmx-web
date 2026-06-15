from datetime import UTC, datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.v1.auth.routes import get_current_user, get_optional_current_user
from app.api.v1.auth.models import User
from app.db.session import get_db
from app.api.v1.quotes.pdf import build_quote_pdf
from app.api.v1.quotes.schemas import QuoteCreate, QuoteOptions, QuoteResult
from app.api.v1.quotes.service import calculate_quote, get_quote_options
from app.api.v1.quotes.repository import (
    create_quote_record,
    get_quote_by_id,
    get_user_quotes,
)
from app.api.v1.quotes.mail import send_quote_email

router = APIRouter(prefix="/quotes", tags=["Quotes"])

DbSession = Annotated[Session, Depends(get_db)]
OptionalUser = Annotated[User | None, Depends(get_optional_current_user)]
RequiredUser = Annotated[User, Depends(get_current_user)]


class SendEmailPayload(BaseModel):
    email: str | None = None


def is_quote_expired(created_at: datetime) -> bool:
    now = datetime.now(created_at.tzinfo) if created_at.tzinfo else datetime.now(UTC)
    return now > created_at + timedelta(days=30)


@router.get("/options", response_model=QuoteOptions)
def list_quote_options():
    return get_quote_options()


@router.post("/", response_model=QuoteResult)
def create_quote(
    payload: QuoteCreate,
    db: DbSession,
    current_user: OptionalUser,
):
    # Calculate the quote result
    result = calculate_quote(payload)

    # Determine user info
    user_id = None
    user_type = "visitor"
    if current_user:
        user_id = current_user.id
        user_type = "user"

    # Save to database
    quote_record = create_quote_record(
        db,
        customer_name=payload.customer_name,
        contact_method=payload.contact_method,
        contact_value=payload.contact_value,
        state=payload.state,
        city=payload.city,
        postal_code=payload.postal_code,
        square_meters=payload.square_meters,
        paint_product=payload.paint_product,
        estimated_price=result.estimated_price,
        payload_json=payload.model_dump(),
        result_json=result.model_dump(),
        user_id=user_id,
        user_type=user_type,
    )

    # Enriched response
    result.id = quote_record.id
    result.created_at = quote_record.created_at.isoformat()
    result.is_expired = False
    return result


@router.get("/my", response_model=list[QuoteResult])
def list_my_quotes(
    db: DbSession,
    current_user: RequiredUser,
):
    quotes = get_user_quotes(db, current_user.id)
    results = []
    for q in quotes:
        try:
            res = QuoteResult.model_validate(q.result_json)
            res.id = q.id
            res.created_at = q.created_at.isoformat()
            res.is_expired = is_quote_expired(q.created_at)
            results.append(res)
        except Exception:
            # Skip invalid/corrupt records if schema changed
            continue
    return results


@router.get("/{quote_id}/pdf")
def get_quote_pdf(
    quote_id: int,
    db: DbSession,
    current_user: OptionalUser,
):
    quote_record = get_quote_by_id(db, quote_id)
    if not quote_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presupuesto no encontrado",
        )

    # Security check: if quote belongs to a registered user, verify ownership
    if quote_record.user_id is not None:
        if not current_user or current_user.id != quote_record.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para ver este presupuesto",
            )

    try:
        payload = QuoteCreate.model_validate(quote_record.payload_json)
        result = QuoteResult.model_validate(quote_record.result_json)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al decodificar la información del presupuesto",
        )

    pdf = build_quote_pdf(payload, result)
    filename = f"precotizacion-{quote_id}.pdf"

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )


@router.post("/{quote_id}/send-email")
async def email_quote_pdf(
    quote_id: int,
    payload: SendEmailPayload,
    db: DbSession,
    current_user: OptionalUser,
):
    quote_record = get_quote_by_id(db, quote_id)
    if not quote_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presupuesto no encontrado",
        )

    # Security check
    if quote_record.user_id is not None:
        if not current_user or current_user.id != quote_record.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para compartir este presupuesto",
            )

    # Determine recipient email
    email_to = payload.email
    if not email_to:
        if quote_record.contact_method == "email":
            email_to = quote_record.contact_value
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionó un correo de destino y el método de contacto de la cotización no es email.",
            )

    try:
        quote_payload = QuoteCreate.model_validate(quote_record.payload_json)
        result = QuoteResult.model_validate(quote_record.result_json)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar la información del presupuesto",
        )

    pdf = build_quote_pdf(quote_payload, result)
    
    sent = await send_quote_email(
        email_to=email_to,
        customer_name=quote_record.customer_name,
        pdf_bytes=pdf,
        filename=f"precotizacion-{quote_id}.pdf"
    )

    if not sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo enviar el correo. Por favor verifique la configuración SMTP del servidor.",
        )

    return {"status": "success", "message": f"Precotización enviada exitosamente a {email_to}"}


# Legacy direct PDF generation from raw payload (backward compatibility)
@router.post("/pdf")
def create_quote_pdf(payload: QuoteCreate):
    quote = calculate_quote(payload)
    pdf = build_quote_pdf(payload, quote)

    filename = "precotizacion-starcolors.pdf"

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )

