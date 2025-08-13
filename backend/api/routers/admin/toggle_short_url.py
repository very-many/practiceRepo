from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import Provide, inject

from backend.api.exceptions import raise_not_found
from backend.container import Container
from backend.schemas.url_schema import URL
from backend.services.url_service import URLService

router: APIRouter = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.put("/{secret_key}/is_active")
@inject
def toggle_short_url(
    secret_key: str, request: Request, url_service: URLService = Depends(Provide[Container.url_service])
) -> dict:
    """Toggles the activation status of a shortened URL identified by its secret key.
    
    Args:
        secret_key (str): The secret key associated with the shortened URL.
        request (Request): The current HTTP request object.
        url_service (URLService): The URL service instance.
        
    Returns:
        dict: A dictionary containing a detail message about the operation's result.
        
    Raises:
        HTTPException: If the shortened URL with the given secret key is not found.
    """

    try:
        db_url: URL | None = url_service.toggle_short_url(secret_key=secret_key)
        message: str = (
            f"Successfully {'reactivated' if db_url.is_active else 'deactivated'} shortened URL for '{db_url.target_url}'"
        )
        return {"detail": message}
    except:
        raise_not_found(request)
