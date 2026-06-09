from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.v1.auth.models import User
from app.api.v1.auth.routes import get_current_user
from app.api.v1.raffle.schemas import (
    ConfirmNumbersRequest,
    RaffleBranchPublic,
    RaffleEntryPublic,
    RaffleNumberPublic,
    RaffleStatusResponse,
    TicketBatchValidateRequest,
    TicketBatchValidateResponse,
    TicketCodeValidationResult,
)
from app.api.v1.raffle.service import (
    confirm_number_selections,
    get_active_raffle,
    get_numbers_by_branch,
    get_raffle_branches,
    get_user_entries,
    validate_ticket_batch,
)
from app.db.session import get_db

router = APIRouter(prefix="/raffle", tags=["raffle"])


@router.get("/status", response_model=RaffleStatusResponse)
def get_raffle_status(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    raffle = get_active_raffle(db)
    branches = get_raffle_branches(db, raffle.id)

    return RaffleStatusResponse(
        raffle_id=raffle.id,
        title=raffle.title,
        prize_title=raffle.prize_title,
        status=raffle.status,
        total_numbers=raffle.total_numbers,
        numbers_per_branch=raffle.numbers_per_branch,
        branches=[RaffleBranchPublic.model_validate(branch) for branch in branches],
    )


@router.get("/branches/{branch_id}/numbers", response_model=list[RaffleNumberPublic])
def get_branch_numbers(
    branch_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    raffle = get_active_raffle(db)
    numbers = get_numbers_by_branch(db, raffle.id, branch_id)

    return numbers


@router.post("/tickets/validate", response_model=TicketBatchValidateResponse)
def validate_tickets(
    data: TicketBatchValidateRequest,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[ User,Depends(get_current_user)],
):
    raffle = get_active_raffle(db)

    batch = validate_ticket_batch(
        db=db,
        raffle=raffle,
        branch_id=data.branch_id,
        codes=data.codes,
        user=current_user,
        ip_address=request.client.host if request.client else None,
    )

    return TicketBatchValidateResponse(
        batch_id=batch.id,
        submitted_count=batch.submitted_count,
        accepted_count=batch.accepted_count,
        rejected_count=batch.rejected_count,
        results=[
            TicketCodeValidationResult(
                ticket_code_id=item.ticket_code_id,
                code_last4=item.code_last4,
                status=item.status,
                reason=item.reason,
            )
            for item in batch.items
        ],
    )


@router.post("/numbers/confirm", response_model=list[RaffleEntryPublic])
def confirm_numbers(
    data: ConfirmNumbersRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[ User,Depends(get_current_user)],
):
    raffle = get_active_raffle(db)

    entries = confirm_number_selections(
        db=db,
        raffle=raffle,
        batch_id=data.batch_id,
        selections=data.selections,
        user=current_user,
    )

    return entries


@router.get("/me/entries", response_model=list[RaffleEntryPublic])
def get_my_raffle_entries(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[ User,Depends(get_current_user)],
):
    raffle = get_active_raffle(db)

    return get_user_entries(
        db=db,
        raffle=raffle,
        user=current_user,
    )
