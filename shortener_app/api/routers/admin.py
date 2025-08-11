from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from shortener_app.api.dependencies import get_db
from shortener_app.api.exceptions import raise_not_found
from shortener_app.services.url_service import URLService
from shortener_app.schemas.url import URLInfo

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/{secret_key}", response_model=URLInfo)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    url_service = URLService(db)

    if db_url := url_service.get_short_url_by_secret_key(secret_key):
        return url_service.build_short_url_info(db_url)
    else:
        raise_not_found(request)


@router.delete("/{secret_key}")
def delete_url(secret_key: str, request: Request, db: Session = Depends(get_db)):
    url_service = URLService(db)

    if db_url := url_service.deactivate_short_url(secret_key=secret_key):
        message = f"Successfully deleted shortened URL for '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise_not_found(request)
