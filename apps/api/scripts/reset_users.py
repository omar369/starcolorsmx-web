import sys
import os
from sqlalchemy import delete, update
from sqlalchemy.engine import CursorResult
from app.db.session import SessionLocal
from app.api.v1.raffle.models import (
    RaffleEntry,
    RaffleTicketBatch,
    RaffleTicketBatchItem,
    RaffleTicketCode,
    RaffleNumber
)
from app.api.v1.auth.models import User

def reset_users() -> None:
    db = SessionLocal()
    try:
        # 1. Borrar participaciones (RaffleEntries) de todos los usuarios
        entries_stmt = delete(RaffleEntry)
        entries_result: CursorResult = db.execute(entries_stmt)
        print(f"Eliminadas {entries_result.rowcount} participaciones (RaffleEntries).")

        # 2. Borrar items de lotes (RaffleTicketBatchItems)
        batch_items_stmt = delete(RaffleTicketBatchItem)
        batch_items_result: CursorResult = db.execute(batch_items_stmt)
        print(f"Eliminados {batch_items_result.rowcount} registros de validación individuales (RaffleTicketBatchItems).")

        # 3. Borrar lotes de tickets (RaffleTicketBatches)
        batches_stmt = delete(RaffleTicketBatch)
        batches_result: CursorResult = db.execute(batches_stmt)
        print(f"Eliminados {batches_result.rowcount} lotes de validación (RaffleTicketBatches).")

        # 4. Borrar todos los códigos de boletos (RaffleTicketCode)
        codes_stmt = delete(RaffleTicketCode)
        codes_result: CursorResult = db.execute(codes_stmt)
        print(f"Eliminados {codes_result.rowcount} códigos de boletos (RaffleTicketCode).")

        # 5. Resetear todos los números del tablero (RaffleNumber)
        numbers_stmt = (
            update(RaffleNumber)
            .values(
                status="available",
                taken_by_user_id=None,
                taken_at=None
            )
        )
        numbers_result: CursorResult = db.execute(numbers_stmt)
        print(f"Restaurados {numbers_result.rowcount} números del tablero a 'available'.")

        # 6. Borrar todos los usuarios de la base de datos
        users_stmt = delete(User)
        users_result: CursorResult = db.execute(users_stmt)
        print(f"Eliminados {users_result.rowcount} usuarios (Users).")

        db.commit()
        print("Reseteo de usuarios completado con éxito. No queda ningún usuario y todos los datos asociados fueron limpiados.")

    except Exception as e:
        db.rollback()
        print(f"Error durante el reseteo de usuarios: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    app_env = os.getenv("APP_ENV", "development").lower()
    
    print("¡ATENCIÓN! Este script BORRARÁ TODOS LOS USUARIOS de la base de datos y limpiará sus participaciones.")
    if app_env == "production":
        print("¡¡ALERTA MÁXIMA!! Detectado entorno de PRODUCCIÓN.")
        confirm = input("Para continuar y ELIMINAR TODOS LOS USUARIOS REALES, escribe exactamente 'ELIMINAR TODOS LOS USUARIOS': ")
        if confirm != "ELIMINAR TODOS LOS USUARIOS":
            print("Operación cancelada por seguridad.")
            sys.exit(0)
    else:
        confirm = input("¿Estás seguro de que deseas eliminar todos los usuarios de desarrollo? (escribe 'si' para continuar): ")
        if confirm.lower() != "si":
            print("Operación cancelada.")
            sys.exit(0)

    reset_users()
