import csv
import os
import sys

from sqlalchemy import select

from app.api.v1.raffle.models import Raffle, RaffleTicketCode
from app.api.v1.raffle.service import hash_code, normalize_code
from app.db.session import SessionLocal


def seed_from_csv(csv_path: str) -> None:
    if not os.path.exists(csv_path):
        print(f"Error: El archivo CSV no existe en {csv_path}")
        sys.exit(1)

    db = SessionLocal()
    try:
        # 1. Obtener sorteo activo
        stmt = select(Raffle).where(Raffle.status == "active")
        raffle = db.execute(stmt).scalar_one_or_none()
        if not raffle:
            print("Error: No se encontró un sorteo activo en la base de datos.")
            return

        print(f"Sorteo activo encontrado: '{raffle.title}' (ID: {raffle.id})")

        # 2. Leer códigos
        codes = []
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)

            # Validar cabecera opcional 'code'
            if header and len(header) > 0 and header[0].lower() == "code":
                pass
            elif header:
                if header[0].strip():
                    codes.append(header[0].strip())

            for row in reader:
                if row and row[0].strip():
                    codes.append(row[0].strip())

        total_codes = len(codes)
        print(f"Se leyeron {total_codes} códigos del archivo CSV.")

        # 3. Procesar e insertar de forma segura
        added_count = 0
        skipped_count = 0

        for idx, raw_code in enumerate(codes, 1):
            normalized = normalize_code(raw_code)
            code_h = hash_code(normalized)
            last4 = normalized[-4:]

            if len(normalized) < 4:
                print(f"Omitido por longitud insuficiente: '{raw_code}'")
                skipped_count += 1
                continue

            # Verificar si ya existe en la BD
            stmt_exists = select(RaffleTicketCode).where(
                RaffleTicketCode.code_hash == code_h
            )
            exists = db.execute(stmt_exists).scalar_one_or_none()

            if exists:
                skipped_count += 1
                continue

            # Insertar registro
            ticket = RaffleTicketCode(
                raffle_id=raffle.id,
                code_hash=code_h,
                code_last4=last4,
                status="available",
            )
            db.add(ticket)
            added_count += 1

            if idx % 100 == 0:
                db.commit()

        db.commit()
        print("Resultado de la importación:")
        print(f"  - Leídos: {total_codes}")
        print(f"  - Nuevos insertados: {added_count}")
        print(f"  - Ya existentes/omitidos: {skipped_count}")

    except Exception as e:
        db.rollback()
        print(f"Error durante la importación: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m scripts.seed_codes_from_csv <ruta.csv>")
        sys.exit(1)

    app_env = os.getenv("APP_ENV", "development").lower()
    if app_env == "production":
        print("¡ATENCIÓN! Detectado entorno de PRODUCCIÓN.")
        confirm = input(
            "¿Confirmas que deseas importar códigos reales? (escribe 'si' para continuar): "
        )
        if confirm.lower() != "si":
            print("Importación cancelada.")
            sys.exit(0)

    seed_from_csv(sys.argv[1])
