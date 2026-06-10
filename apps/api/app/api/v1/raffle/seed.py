from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.raffle.models import (
    Raffle,
    RaffleBranch,
    RaffleNumber,
    RaffleTicketCode,
)
from app.api.v1.raffle.service import hash_code, normalize_code


def seed_raffle(db: Session) -> None:
    existing_raffle = db.execute(
        select(Raffle).where(Raffle.slug == "sorteo-temporada-2026")
    ).scalar_one_or_none()

    if existing_raffle:
        raffle = existing_raffle
        if raffle.prize_title != 'Gana SMART TV':
            raffle.prize_title = 'Gana SMART TV'
        if raffle.max_batches_per_user_24h != 10:
            raffle.max_batches_per_user_24h = 10
    else:
        raffle = Raffle(
            title="Sorteo de temporada",
            slug="sorteo-temporada-2026",
            prize_title='Gana SMART TV',
            status="active",
            total_numbers=495,
            numbers_per_branch=165,
            max_batches_per_user_24h=10,
        )

        db.add(raffle)
        db.flush()

        branches = [
            RaffleBranch(
                raffle_id=raffle.id,
                name="Sucursal Centro",
                slug="centro",
                image_url=None,
                number_start=1,
                number_end=165,
                sort_order=1,
            ),
            RaffleBranch(
                raffle_id=raffle.id,
                name="Sucursal Norte",
                slug="norte",
                image_url=None,
                number_start=166,
                number_end=330,
                sort_order=2,
            ),
            RaffleBranch(
                raffle_id=raffle.id,
                name="Sucursal Sur",
                slug="sur",
                image_url=None,
                number_start=331,
                number_end=495,
                sort_order=3,
            ),
        ]

        db.add_all(branches)
        db.flush()

        for branch in branches:
            for number in range(branch.number_start, branch.number_end + 1):
                db.add(
                    RaffleNumber(
                        raffle_id=raffle.id,
                        branch_id=branch.id,
                        number=number,
                        status="available",
                    )
                )

    existing_codes_count = (
        db.execute(
            select(RaffleTicketCode).where(RaffleTicketCode.raffle_id == raffle.id)
        )
        .scalars()
        .all()
    )

    if not existing_codes_count:
        demo_codes = [
            "A7K2P9",
            "M4X8Q1",
            "Z9T3L6",
            "C2V7N5",
            "R8B1Y4",
            "H6D9W2",
            "P3Q5J8",
            "L1S7K0",
            "V9E2C6",
            "N4G8A3",
            "T6M1X9",
            "B8R5Z2",
            "K2Y7D4",
            "Q5L9P1",
            "W3C6H8",
        ]

        for code in demo_codes:
            normalized_code = normalize_code(code)

            db.add(
                RaffleTicketCode(
                    raffle_id=raffle.id,
                    code_hash=hash_code(normalized_code),
                    code_last4=normalized_code[-4:],
                    status="available",
                )
            )

    db.commit()
