from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from shortener_app.api.dependencies import get_db
from shortener_app.api.exceptions import raise_not_found
from shortener_app.schemas.url import URLBase, URLInfo
from shortener_app.services.url_service import URLService

router = APIRouter(
    tags=["URLs"],
)


@router.post("/url", response_model=URLInfo)
def create_short_url(url: URLBase, db: Session = Depends(get_db)):
    url_service = URLService(db)
    db_url = url_service.create_short_url(url)
    return url_service.build_short_url_info(db_url)


@router.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):
    url_service = URLService(db)

    if db_url := url_service.get_short_url_by_key(url_key):
        url_service.increment_clicks(db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)
