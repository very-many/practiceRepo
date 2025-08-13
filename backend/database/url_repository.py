from sqlalchemy.orm import sessionmaker
from backend.database.models.url_database_model import URL


class URLRepository:
    """Repository for managing URL records in the database.

    Functions:
    - __init__: Initialize the repository with a database session factory.
    - create: Create a new URL record.
    - get_by_key: Retrieve a URL record by its key.
    - get_by_secret_key: Retrieve a URL record by its secret key.
    - increment_clicks: Increment the click counter for a URL.
    - delete_by_secret_key: Delete a URL record by its secret key.
    - toggle_active_by_secret_key: Toggle the active status of a URL.
    """

    def __init__(self, session_factory: sessionmaker):
        """Initialize the URLRepository with a database session factory.

        Args:
            session_factory (sessionmaker): The session factory for creating database sessions.
        """

        self.session_factory = session_factory

    def create(self, url_data: dict) -> URL:
        """Create a new URL record in the database.

        Args:
            url_data (dict): The data for the new URL record.

        Returns:
            URL: The created URL record.
        """

        with self.session_factory() as db:
            try:
                db_url = URL(**url_data)
                db.add(db_url)
                db.commit()  # Commit within the same session
                db.refresh(db_url)  # Refresh within the same session
                return db_url
            except Exception:
                db.rollback()
                raise

    def get_by_key(self, key: str) -> URL | None:
        """Retrieve a URL record by its key.

        Args:
            key (str): The unique key for the shortened URL.

        Returns:
            (URL | None): The URL record if found, None otherwise.
        """

        with self.session_factory() as db:
            return db.query(URL).filter(URL.key == key, URL.is_active == True).first()

    def get_by_secret_key(self, secret_key: str) -> URL | None:
        """Retrieve a URL record by its secret key.

        Args:
            secret_key (str): The secret key associated with the shortened URL.

        Returns:
            (URL | None): The URL record if found, None otherwise.
        """

        with self.session_factory() as db:
            return db.query(URL).filter(URL.secret_key == secret_key).first()

    def increment_clicks(self, key: str) -> URL:
        """Increment click counter for a URL by its key.

        Args:
            key (str): The unique key for the shortened URL.

        Returns:
            URL: The updated URL record.
        """

        with self.session_factory() as db:
            try:
                db_url = (
                    db.query(URL).filter(URL.key == key, URL.is_active == True).first()
                )
                if db_url:
                    print("Incrementing clicks for URL:", db_url.key)
                    db_url.clicks += 1
                    db.commit()
                    db.refresh(db_url)
                return db_url
            except Exception:
                db.rollback()
                raise

    def delete_by_secret_key(self, secret_key: str) -> URL | None:
        """Delete a URL record by its secret key.

        Args:
            secret_key (str): The secret key associated with the shortened URL.

        Returns:
            (URL | None): The deleted URL record if found, None otherwise.
        """
        
        with self.session_factory() as db:
            try:
                # Query within the SAME session, not calling self.get_by_secret_key()
                db_url = db.query(URL).filter(URL.secret_key == secret_key).first()
                if db_url:
                    db.delete(db_url)
                    db.commit()
                return db_url
            except Exception:
                db.rollback()
                raise

    def toggle_active_by_secret_key(self, secret_key: str) -> URL | None:
        """Toggle the active status of a URL record by its secret key.

        Args:
            secret_key (str): The secret key associated with the shortened URL.

        Returns:
            (URL | None): The updated URL record if found, None otherwise.
        """
        
        with self.session_factory() as db:
            try:
                db_url = db.query(URL).filter(URL.secret_key == secret_key).first()
                if db_url:
                    db_url.is_active = not db_url.is_active
                    db.commit()
                    db.refresh(db_url)
                return db_url
            except Exception:
                db.rollback()
                raise
