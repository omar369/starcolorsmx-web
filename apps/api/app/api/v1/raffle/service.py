import hashlib
from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.auth.models import User
from app.api.v1.raffle.models import (
    Raffle,
    RaffleBranch,
    RaffleEntry,
    RaffleNumber,
    RaffleTicketBatch,
    RaffleTicketBatchItem,
    RaffleTicketCode,
    utc_now,
)


def normalize_code(code: str) -> str:
    return code.strip().upper().replace(" ", "")


def hash_code(code: str) -> str:
    normalized = normalize_code(code)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def get_active_raffle(db: Session) -> Raffle:
    stmt = select(Raffle).where(Raffle.status == "active")
    raffle = db.execute(stmt).scalar_one_or_none()

    if not raffle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay sorteo activo por el momento.",
        )

    return raffle


def get_raffle_branches(db: Session, raffle_id: int) -> list[RaffleBranch]:
    stmt = (
        select(RaffleBranch)
        .where(
            RaffleBranch.raffle_id == raffle_id,
            RaffleBranch.status == "active",
        )
        .order_by(RaffleBranch.sort_order)
    )

    return list(db.execute(stmt).scalars().all())


def get_branch_by_id(db: Session, raffle_id: int, branch_id: int) -> RaffleBranch:
    stmt = select(RaffleBranch).where(
        RaffleBranch.id == branch_id,
        RaffleBranch.raffle_id == raffle_id,
        RaffleBranch.status == "active",
    )

    branch = db.execute(stmt).scalar_one_or_none()

    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sucursal no encontrada.",
        )

    return branch


def get_numbers_by_branch(
    db: Session,
    raffle_id: int,
    branch_id: int,
) -> list[RaffleNumber]:
    stmt = (
        select(RaffleNumber)
        .where(
            RaffleNumber.raffle_id == raffle_id,
            RaffleNumber.branch_id == branch_id,
        )
        .order_by(RaffleNumber.number)
    )

    return list(db.execute(stmt).scalars().all())


def count_user_batches_last_24h(
    db: Session,
    raffle_id: int,
    user_id: int,
) -> int:
    since = utc_now() - timedelta(hours=24)

    stmt = select(RaffleTicketBatch).where(
        RaffleTicketBatch.raffle_id == raffle_id,
        RaffleTicketBatch.user_id == user_id,
        RaffleTicketBatch.created_at >= since,
    )

    return len(db.execute(stmt).scalars().all())


def validate_ticket_batch(
    db: Session,
    raffle: Raffle,
    branch_id: int,
    codes: list[str],
    user: User,
    ip_address: str | None = None,
) -> RaffleTicketBatch:
    get_branch_by_id(db, raffle.id, branch_id)

    if len(codes) > raffle.max_codes_per_batch:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Solo puedes cargar hasta {raffle.max_codes_per_batch} boletos.",
        )

    batch_count = count_user_batches_last_24h(db, raffle.id, user.id)

    if batch_count >= raffle.max_batches_per_user_24h:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Alcanzaste el límite de cargas por 24 horas.",
        )

    batch = RaffleTicketBatch(
        raffle_id=raffle.id,
        user_id=user.id,
        branch_id=branch_id,
        ip_address=ip_address,
        submitted_count=len(codes),
        accepted_count=0,
        rejected_count=0,
    )

    db.add(batch)
    db.flush()

    seen_hashes: set[str] = set()

    for raw_code in codes:
        code_hash = hash_code(raw_code)
        code_last4 = normalize_code(raw_code)[-4:]

        if code_hash in seen_hashes:
            item = RaffleTicketBatchItem(
                batch_id=batch.id,
                ticket_code_id=None,
                code_hash=code_hash,
                code_last4=code_last4,
                status="rejected",
                reason="duplicate_in_batch",
            )
            batch.rejected_count += 1
            db.add(item)
            continue

        seen_hashes.add(code_hash)

        stmt = select(RaffleTicketCode).where(
            RaffleTicketCode.raffle_id == raffle.id,
            RaffleTicketCode.code_hash == code_hash,
        )
        ticket_code = db.execute(stmt).scalar_one_or_none()

        if not ticket_code:
            item = RaffleTicketBatchItem(
                batch_id=batch.id,
                ticket_code_id=None,
                code_hash=code_hash,
                code_last4=code_last4,
                status="rejected",
                reason="not_found",
            )
            batch.rejected_count += 1
            db.add(item)
            continue

        if ticket_code.status != "available":
            item = RaffleTicketBatchItem(
                batch_id=batch.id,
                ticket_code_id=ticket_code.id,
                code_hash=code_hash,
                code_last4=code_last4,
                status="rejected",
                reason="already_used",
            )
            batch.rejected_count += 1
            db.add(item)
            continue

        item = RaffleTicketBatchItem(
            batch_id=batch.id,
            ticket_code_id=ticket_code.id,
            code_hash=code_hash,
            code_last4=code_last4,
            status="accepted",
            reason=None,
        )

        batch.accepted_count += 1
        db.add(item)

    db.commit()
    db.refresh(batch)

    return batch


def get_batch_accepted_items(
    db: Session,
    batch_id: int,
    user_id: int,
) -> list[RaffleTicketBatchItem]:
    stmt = (
        select(RaffleTicketBatchItem)
        .join(RaffleTicketBatch)
        .where(
            RaffleTicketBatch.id == batch_id,
            RaffleTicketBatch.user_id == user_id,
            RaffleTicketBatchItem.status == "accepted",
        )
    )

    return list(db.execute(stmt).scalars().all())


def confirm_number_selections(
    db: Session,
    raffle: Raffle,
    batch_id: int,
    selections: list,
    user: User,
) -> list[RaffleEntry]:
    accepted_items = get_batch_accepted_items(db, batch_id, user.id)

    accepted_ticket_ids = {
        item.ticket_code_id
        for item in accepted_items
        if item.ticket_code_id is not None
    }

    if len(selections) != len(accepted_ticket_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes elegir un número por cada boleto válido.",
        )

    entries: list[RaffleEntry] = []

    for selection in selections:
        if selection.ticket_code_id not in accepted_ticket_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uno de los boletos no pertenece a esta carga.",
            )

        ticket_code = db.get(RaffleTicketCode, selection.ticket_code_id)
        raffle_number = db.get(RaffleNumber, selection.raffle_number_id)

        if not ticket_code or ticket_code.raffle_id != raffle.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Boleto no encontrado.",
            )

        if not raffle_number or raffle_number.raffle_id != raffle.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Número no encontrado.",
            )

        if ticket_code.status != "available":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Uno de los boletos ya fue usado.",
            )

        if raffle_number.status != "available":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Uno de los números acaba de ser tomado.",
            )

        ticket_code.status = "used"
        ticket_code.used_by_user_id = user.id
        ticket_code.used_at = utc_now()

        raffle_number.status = "taken"
        raffle_number.taken_by_user_id = user.id
        raffle_number.taken_at = utc_now()

        entry = RaffleEntry(
            raffle_id=raffle.id,
            user_id=user.id,
            branch_id=raffle_number.branch_id,
            ticket_code_id=ticket_code.id,
            raffle_number_id=raffle_number.id,
            batch_id=batch_id,
            selected_number=raffle_number.number,
        )

        db.add(entry)
        entries.append(entry)

    db.commit()

    for entry in entries:
        db.refresh(entry)

    return entries


def get_user_entries(
    db: Session,
    raffle: Raffle,
    user: User,
) -> list[RaffleEntry]:
    stmt = (
        select(RaffleEntry)
        .where(
            RaffleEntry.raffle_id == raffle.id,
            RaffleEntry.user_id == user.id,
        )
        .order_by(RaffleEntry.created_at.desc())
    )

    return list(db.execute(stmt).scalars().all())
