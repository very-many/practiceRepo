import secrets
import string
from sqlalchemy.orm import Session

from ..models.url import URL

class KeyService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_random_key(self, length: int = 5) -> str:
        """Generate random key with specified length"""
        chars = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(chars) for _ in range(length))
    
    def create_unique_key(self) -> str:
        """Create unique random key that doesn't exist in database"""
        key = self.create_random_key()
        while self._key_exists(key):
            key = self.create_random_key()
        return key
    
    def create_secret_key(self, key: str, length: int = 8) -> str:
        """Create secret key based on main key"""
        random_part = self.create_random_key(length)
        return f"{key}_{random_part}"
    
    def _key_exists(self, key: str) -> bool:
        """Check if key already exists in database"""
        return (
            self.db.query(URL)
            .filter(URL.key == key)
            .first() is not None
        )