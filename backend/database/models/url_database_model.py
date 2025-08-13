from sqlalchemy import Boolean, Column, Integer, String

from backend.database.database import Base

class URL(Base):
    """Represents a URL entity with additional metadata.

    Attributes:
        id (int): The unique identifier for the URL.
        key (str): The unique key for the shortened URL.
        secret_key (str): The secret key for the shortened URL.
        target_url (str): The original URL that is to be shortened or processed.
        is_active (bool): Indicates whether the URL is currently active.
        clicks (int): The number of times the shortened URL has been accessed.
    """
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)