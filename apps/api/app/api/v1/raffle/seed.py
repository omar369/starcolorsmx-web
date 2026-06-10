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

    # Asegurar sucursales actualizadas
    expected_branches = [
        {
            "slug": "burocrata",
            "name": "Burocrata",
            "image_url": "/images/contacto/burocrata.jpg",
            "number_start": 1,
            "number_end": 165,
            "sort_order": 1,
        },
        {
            "slug": "pueblito",
            "name": "El Pueblito",
            "image_url": "/images/contacto/pueblito.jpg",
            "number_start": 166,
            "number_end": 330,
            "sort_order": 2,
        },
        {
            "slug": "constituyentes",
            "name": "Constituyentes",
            "image_url": "/images/contacto/constituyentes.jpg",
            "number_start": 331,
            "number_end": 495,
            "sort_order": 3,
        },
    ]

    for data in expected_branches:
        branch = db.execute(
            select(RaffleBranch).where(
                RaffleBranch.raffle_id == raffle.id,
                RaffleBranch.sort_order == data["sort_order"]
            )
        ).scalar_one_or_none()

        if branch:
            branch.name = data["name"]
            branch.slug = data["slug"]
            branch.image_url = data["image_url"]
            branch.number_start = data["number_start"]
            branch.number_end = data["number_end"]
        else:
            branch = RaffleBranch(
                raffle_id=raffle.id,
                name=data["name"],
                slug=data["slug"],
                image_url=data["image_url"],
                number_start=data["number_start"],
                number_end=data["number_end"],
                sort_order=data["sort_order"],
            )
            db.add(branch)
        db.flush()

        # Asegurar números
        for number in range(branch.number_start, branch.number_end + 1):
            existing_number = db.execute(
                select(RaffleNumber).where(
                    RaffleNumber.raffle_id == raffle.id,
                    RaffleNumber.number == number
                )
            ).scalar_one_or_none()

            if not existing_number:
                db.add(
                    RaffleNumber(
                        raffle_id=raffle.id,
                        branch_id=branch.id,
                        number=number,
                        status="available",
                    )
                )

    db.commit()

