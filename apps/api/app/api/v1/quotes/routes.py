from fastapi import APIRouter, Response

from app.api.v1.quotes.pdf import build_quote_pdf
from app.api.v1.quotes.schemas import QuoteCreate, QuoteOptions, QuoteResult
from app.api.v1.quotes.service import calculate_quote, get_quote_options

router = APIRouter(prefix="/quotes", tags=["Quotes"])


@router.get("/options", response_model=QuoteOptions)
def list_quote_options():
    return get_quote_options()


@router.post("/", response_model=QuoteResult)
def create_quote(payload: QuoteCreate):
    return calculate_quote(payload)


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
