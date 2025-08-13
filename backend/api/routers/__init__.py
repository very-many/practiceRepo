from fastapi import APIRouter

from backend.api.routers import url
from backend.api.routers import admin
from backend.api.routers import health

router = APIRouter()

# Add all related routers
router.include_router(health.router)
router.include_router(url.router)
router.include_router(admin.router)

__all__ = ["router"]