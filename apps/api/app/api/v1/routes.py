from fastapi import APIRouter

from app.api.v1.auth.routes import router as auth_router
from app.api.v1.health.routes import router as health_router
from app.api.v1.quotes.routes import router as quotes_router
from app.api.v1.raffle.routes import router as raffle_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(health_router)
router.include_router(quotes_router)
router.include_router(raffle_router)
