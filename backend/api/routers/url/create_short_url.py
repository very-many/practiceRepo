from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject


from backend.schemas.url_schema import URLBase, URLInfo
from backend.services.url_service import URLService
from backend.container import Container
from backend.api.exceptions import raise_bad_request


router = APIRouter(
    tags=["URLs"],
)


@router.post("/url", response_model=URLInfo)
@inject
def create_short_url(url: URLBase, url_service: URLService = Depends(Provide[Container.url_service])) -> URLInfo:
    """Create a shortened URL.

    Args:
        url (URLBase): The original URL to be shortened.
        url_service (URLService, optional): The URL service instance. Defaults to Depends(Provide[Container.url_service]).

    Returns:
        URLInfo: The information about the created shortened URL.
    """
    
    try:
        short_url = url_service.create_short_url(url)
        return url_service.build_short_url_info(short_url)
    except Exception as e:
        raise_bad_request(message=f"Failed to create short URL: {str(e)}")