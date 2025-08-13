from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from dependency_injector.wiring import Provide, inject

from backend.container import Container
from backend.api.exceptions import  raise_not_found
from backend.schemas.url_schema import URL
from backend.services.url_service import URLService

router = APIRouter(
    tags=["URLs"],
)


@router.get("/{url_key}")
@inject
def forward_to_target_url(
    url_key: str, request: Request, url_service: URLService = Depends(Provide[Container.url_service])
) -> RedirectResponse:
    """Redirect to the target URL.

    Args:
        url_key (str): The unique key for the shortened URL.
        request (Request): The incoming request object.
        url_service (URLService, optional): The URL service instance. Defaults to Depends(Provide[Container.url_service]).

    Returns:
        RedirectResponse: The redirect response to the target URL.
    """
    try:
        url_service.increment_clicks(url_key)
        db_url: URL | None = url_service.get_short_url_by_key(url_key)
        return RedirectResponse(db_url.target_url)
    except:
        raise_not_found(request)
