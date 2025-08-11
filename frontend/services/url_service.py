from frontend.services.api import create_short_url, delete_short_url, get_admin_info, toggle_short_url
from typing import Dict, Any


class URLService:
    """Service for URL shortening operations"""
    
    @staticmethod
    def shorten_url(url: str) -> Dict[str, Any]:
        if not url or not url.strip():
            raise ValueError("URL cannot be empty")
            
        result = create_short_url(url)
        return result
    
    @staticmethod
    def get_url_analytics(admin_key: str) -> Dict[str, Any]:
        if not admin_key or not admin_key.strip():
            raise ValueError("Admin key cannot be empty")
            
        result = get_admin_info(admin_key)
        return result
    
    @staticmethod
    def delete_short_url(secret_key: str) -> None:
        if not secret_key or not secret_key.strip():
            raise ValueError("Secret key cannot be empty")

        delete_short_url(secret_key)

    @staticmethod
    def toggle_short_url(secret_key: str) -> None:
        if not secret_key or not secret_key.strip():
            raise ValueError("Secret key cannot be empty")

        toggle_short_url(secret_key)
