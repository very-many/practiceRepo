from sqlalchemy.orm import Session
from shortener_app.database import SessionLocal

from typing import Generator

def get_db() -> Generator[Session, None, None]:
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()