from fastapi import APIRouter
from .create_short_url import router as create_short_url_router
from .forward_to_target_url import router as forward_to_target_url_router

router = APIRouter()

# Add all URL-related routers
router.include_router(create_short_url_router)
router.include_router(forward_to_target_url_router)

__all__ = ["router"]