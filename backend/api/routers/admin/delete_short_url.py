from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import Provide, inject
from httpcore import URL

from backend.api.exceptions import raise_not_found
from backend.container import Container
from backend.services.url_service import URLService

router: APIRouter = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.delete("/{secret_key}")
@inject
def delete_short_url(
    secret_key: str, request: Request, url_service: URLService = Depends(Provide[Container.url_service])
) -> dict:
    """Delete a shortened URL.

    Args:
        secret_key (str): The secret key of the shortened URL.
        request (Request): The FastAPI request object.
        url_service (URLService): The URL service instance.

    Returns:
        dict: A message indicating the result of the deletion.

    Raises:
        HTTPException: If the shortened URL with the given secret key is not found.
    """
    try:
        db_url: URL | None = url_service.delete_short_url(secret_key=secret_key)
        message: str = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    except:
        raise_not_found(request)
