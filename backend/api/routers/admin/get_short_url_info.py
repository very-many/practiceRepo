from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import Provide, inject

from backend.container import Container
from backend.api.exceptions import raise_not_found
from backend.services.url_service import URLService
from backend.schemas.url_schema import URL, URLInfo

router: APIRouter = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/{secret_key}", response_model=URLInfo)
@inject
def get_short_url_info(
    secret_key: str, request: Request, url_service: URLService = Depends(Provide[Container.url_service])
) -> URLInfo:
    """Get information about a shortened URL.

    Args:
        secret_key (str): The secret key of the shortened URL.
        request (Request): The FastAPI request object.
        url_service (URLService): The URL service instance.

    Returns:
        URLInfo: The information about the shortened URL.

    Raises:
        HTTPException: If the shortened URL with the given secret key is not found.
    """

    try:
        db_url: URL | None = url_service.get_short_url_by_secret_key(secret_key)
        return url_service.build_short_url_info(db_url)
    except:
        raise_not_found(request)
