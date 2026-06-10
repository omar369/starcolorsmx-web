import sys
import os
from sqlalchemy import select, delete, update
from app.db.session import SessionLocal
from app.api.v1.raffle.models import (
    Raffle,
    RaffleEntry,
    RaffleTicketBatch,
    RaffleTicketBatchItem,
    RaffleTicketCode,
    RaffleNumber
)

def reset_raffle() -> None:
    db = SessionLocal()
    try:
        # 1. Obtener sorteo activo
        stmt = select(Raffle).where(Raffle.status == "active")
        raffle = db.execute(stmt).scalar_one_or_none()
        if not raffle:
            print("Error: No se encontró un sorteo activo.")
            return

        print(f"Sorteo activo encontrado: '{raffle.title}' (ID: {raffle.id})")

        # 2. Borrar participaciones (RaffleEntries)
        entries_stmt = delete(RaffleEntry).where(RaffleEntry.raffle_id == raffle.id)
        entries_result = db.execute(entries_stmt)
        print(f"Eliminadas {entries_result.rowcount} participaciones (RaffleEntries).")

        # 3. Borrar items de lotes (RaffleTicketBatchItems)
        batch_items_stmt = delete(RaffleTicketBatchItem)
        batch_items_result = db.execute(batch_items_stmt)
        print(f"Eliminados {batch_items_result.rowcount} registros de validación individuales (RaffleTicketBatchItems).")

        # 4. Borrar lotes de tickets (RaffleTicketBatches)
        batches_stmt = delete(RaffleTicketBatch).where(RaffleTicketBatch.raffle_id == raffle.id)
        batches_result = db.execute(batches_stmt)
        print(f"Eliminados {batches_result.rowcount} lotes de validación (RaffleTicketBatches).")

        # 5. Resetear códigos de boletos (RaffleTicketCode)
        codes_stmt = (
            update(RaffleTicketCode)
            .where(RaffleTicketCode.raffle_id == raffle.id)
            .values(
                status="available",
                used_by_user_id=None,
                used_at=None
            )
        )
        codes_result = db.execute(codes_stmt)
        print(f"Restaurados {codes_result.rowcount} códigos de boletos a 'available'.")

        # 6. Resetear números del tablero (RaffleNumber)
        numbers_stmt = (
            update(RaffleNumber)
            .where(RaffleNumber.raffle_id == raffle.id)
            .values(
                status="available",
                taken_by_user_id=None,
                taken_at=None
            )
        )
        numbers_result = db.execute(numbers_stmt)
        print(f"Restaurados {numbers_result.rowcount} números del tablero a 'available'.")

        db.commit()
        print("Reseteo completado con éxito. Todos los códigos y números vuelven a estar libres.")

    except Exception as e:
        db.rollback()
        print(f"Error durante el reseteo: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    app_env = os.getenv("APP_ENV", "development").lower()
    
    print("¡ATENCIÓN! Este script borrará todas las participaciones de los usuarios y liberará todos los números.")
    if app_env == "production":
        print("¡¡ALERTA MÁXIMA!! Detectado entorno de PRODUCCIÓN.")
        confirm = input("Para continuar y BORRAR DATOS REALES de clientes, escribe exactamente 'BORRAR DATOS REALES': ")
        if confirm != "BORRAR DATOS REALES":
            print("Operación cancelada por seguridad.")
            sys.exit(0)
    else:
        confirm = input("¿Estás seguro de que deseas resetear el sorteo de desarrollo? (escribe 'si' para continuar): ")
        if confirm.lower() != "si":
            print("Operación cancelada.")
            sys.exit(0)

    reset_raffle()
