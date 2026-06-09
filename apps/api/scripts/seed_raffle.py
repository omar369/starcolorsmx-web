from app.api.v1.raffle.seed import seed_raffle
from app.db.session import SessionLocal


def main() -> None:
    db = SessionLocal()

    try:
        seed_raffle(db)
        print("Raffle seed completed.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
