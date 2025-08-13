import secrets
import string

from backend.database.models.url_database_model import URL


class KeyService:
    """Service class responsible for managing URL shortening keys.
    
    Functions:
        - __init__: Initializes with database session.
        - create_random_key: Generate a random key.
        - create_unique_key: Generate a unique key.
        - create_secret_key: Generate a secret key.
    """

    def __init__(self, session_factory):
        """Initialize KeyService with a database session.

        Args:
            db (Database): The database session to use for key management.
        """
        self.session_factory = session_factory

    def create_random_key(self, length: int = 5) -> str:
        """Generate a random key with the specified length.

        Args:
            length (int, optional): The length of the key to generate. Defaults to 5.

        Returns:
            str: The generated random key.
        """
        chars = string.ascii_uppercase + string.digits
        return "".join(secrets.choice(chars) for _ in range(length))

    def create_unique_key(self) -> str:
        """Create a unique 5 characters long random key that doesn't exist in the database.

        Returns:
            str: The unique random key.
        """
        key = self.create_random_key()
        while self._key_exists(key):
            key = self.create_random_key()
        return key

    def create_secret_key(self, key: str, length: int = 8) -> str:
        """Create a secret key based on the main key.

        Args:
            key (str): The main key to base the secret key on.
            length (int, optional): The length of the random part of the secret key. Defaults to 8.

        Returns:
            str: The generated secret key.
        """
        random_part = self.create_random_key(length)
        return f"{key}_{random_part}"

    def _key_exists(self, key: str) -> bool:
        """Check if the key already exists in the database.

        Args:
            key (str): The key to check for existence.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        with self.session_factory() as db:
            # Assuming URL is the model class for URLs in the database
            # and it has a 'key' field.
            return db.query(URL).filter(URL.key == key).first() is not None