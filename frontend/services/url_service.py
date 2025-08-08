from frontend.services.api import create_url, get_admin_info
from typing import Dict, Any


class URLService:
    """Service for URL shortening operations"""
    
    @staticmethod
    def shorten_url(url: str) -> Dict[str, Any]:
        if not url or not url.strip():
            raise ValueError("URL cannot be empty")
            
        result = create_url(url)
        return result
    
    @staticmethod
    def get_url_analytics(admin_key: str) -> Dict[str, Any]:
        if not admin_key or not admin_key.strip():
            raise ValueError("Admin key cannot be empty")
            
        result = get_admin_info(admin_key)
        return result
