from fastapi import APIRouter
from backend.api.routers.admin.get_short_url_info import router as get_short_url_info_router
from backend.api.routers.admin.toggle_short_url import router as toggle_short_url_router
from backend.api.routers.admin.delete_short_url import router as delete_short_url_router

router = APIRouter()

# Add all Admin-related routers
router.include_router(get_short_url_info_router)
router.include_router(toggle_short_url_router)
router.include_router(delete_short_url_router)

__all__ = ["router"]