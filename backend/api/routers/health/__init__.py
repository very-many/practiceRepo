from fastapi import APIRouter
from backend.api.routers.health.health_check import router as health_check_router

router = APIRouter()

# Add all Health-related routers
router.include_router(health_check_router)

__all__ = ["router"]
