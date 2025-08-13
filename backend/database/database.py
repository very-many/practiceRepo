from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Database:
    """Database connection and session management.
    
    Functions:
        - __init__: Initialize the database connection.
        - create_tables: Create all tables in the database.
    """
    def __init__(self, db_url: str):
        """Initialize the database connection.

        Args:
            db_url (str): The database URL.
        """
        self._engine = create_engine(
            db_url, connect_args={"check_same_thread": False}
        )
        self._session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )
    
    def create_tables(self):
        """Create all tables in the database."""
        Base.metadata.create_all(bind=self._engine)