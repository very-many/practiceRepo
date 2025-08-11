from sqlalchemy.orm import Session
from starlette.datastructures import URL as StarletteURL
import validators

from ..config import get_settings
from ..models.url import URL
from ..schemas.url import URLBase, URLInfo
from ..services.key_service import KeyService
from ..api.exceptions import InvalidURLException

class URLService:
    def __init__(self, db: Session):
        self.db = db
        self.key_service = KeyService(db)
    
    def create_short_url(self, url_data: URLBase) -> URL:
        """Create a new shortened URL"""
        if not validators.url(url_data.target_url):
            raise InvalidURLException("Provided URL is not valid")
        
        key = self.key_service.create_unique_key()
        secret_key = self.key_service.create_secret_key(key)
        
        db_url = URL(
            target_url=url_data.target_url,
            key=key,
            secret_key=secret_key
        )
        
        self.db.add(db_url)
        self.db.commit()
        self.db.refresh(db_url)
        
        return db_url
    
    def get_short_url_by_key(self, url_key: str) -> URL | None:
        """Get active URL by key"""
        return (
            self.db.query(URL)
            .filter(URL.key == url_key, URL.is_active == True)
            .first()
        )

    def get_short_url_by_secret_key(self, secret_key: str) -> URL | None:
        """Get active URL by secret key"""
        return (
            self.db.query(URL)
            .filter(URL.secret_key == secret_key, URL.is_active == True)
            .first()
        )
    
    def increment_clicks(self, db_url: URL) -> URL:
        """Increment click counter"""
        db_url.clicks += 1
        self.db.commit()
        self.db.refresh(db_url)
        return db_url

    def deactivate_short_url(self, secret_key: str) -> URL | None:
        """Deactivate URL by secret key"""
        db_url = self.get_url_by_secret_key(secret_key)
        if db_url:
            db_url.is_active = False
            self.db.commit()
            self.db.refresh(db_url)
        return db_url

    def build_short_url_info(self, db_url: URL) -> URLInfo:
        """Build URLInfo response with full URLs"""
        base_url = StarletteURL(get_settings().base_url)
                
        return URLInfo(
            target_url=db_url.target_url,
            is_active=db_url.is_active,
            clicks=db_url.clicks,
            url=str(base_url.replace(path=f"/{db_url.key}")),
            admin_url=str(base_url.replace(path=f"/admin/{db_url.secret_key}"))
        )