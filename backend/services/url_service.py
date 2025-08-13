from starlette.datastructures import URL as StarletteURL
import validators

from backend.config import Settings
from backend.database.models.url_database_model import URL
from backend.schemas.url_schema import URLBase, URLInfo
from backend.services.key_service import KeyService
from backend.api.exceptions import raise_bad_request
from backend.database.url_repository import URLRepository


class URLService:
    """Service class responsible for managing URLs in the database and executing URL shortening operations.

    Functions:
        - __init__: Initializes with database session and key service.
        - create_short_url: Create a new shortened URL.
        - get_short_url_by_key: Retrieve an active URL by its unique key.
        - get_short_url_by_secret_key: Retrieve an active URL by its secret key.
        - increment_clicks: Increment the click counter for a URL.
        - delete_short_url: Deactivate a URL by its secret key.
        - toggle_short_url: Toggle the activation state of a URL by its secret key.
        - build_short_url_info: Build a URLInfo object from a URL.
    """

    def __init__(
        self, key_service: KeyService, settings: Settings, url_repository: URLRepository
    ):
        """Initialize URLService with a database session.

        Args:
            db (Session): The database session to use for URL management.
            key_service (KeyService): The service responsible for generating unique keys.
        """
        
        self.url_repository = url_repository
        self.key_service = key_service
        self.settings = settings

    def create_short_url(self, url_data: URLBase) -> URL:
        """Create a new shortened URL.

        Args:
            url_data (URLBase): The URL data to create the shortened URL for.

        Returns:
            URL: The created shortened URL.

        Raises:
            HTTPException: If the provided URL is not valid.
        """

        if not validators.url(url_data.target_url):
            raise raise_bad_request("Provided URL is not valid")

        key: str = self.key_service.create_unique_key()
        secret_key: str = self.key_service.create_secret_key(key)

        return self.url_repository.create(
            {
                "target_url": url_data.target_url,
                "key": key,
                "secret_key": secret_key,
            }
        )

    def get_short_url_by_key(self, url_key: str) -> URL | None:
        """Get active URL by key.

        Args:
            url_key (str): The key of the URL to retrieve.

        Returns:
            (URL | None): The retrieved URL or None if not found.
        """
        return self.url_repository.get_by_key(url_key)

    def get_short_url_by_secret_key(self, secret_key: str) -> URL | None:
        """Get active URL by secret key.

        Args:
            secret_key (str): The secret key of the URL to retrieve.

        Returns:
            (URL | None): The retrieved URL or None if not found.
        """

        return self.url_repository.get_by_secret_key(secret_key)

    def increment_clicks(self, key: str) -> URL:
        """Increment click counter for a URL.

        Args:
            key (str): The key of the URL to increment clicks for.

        Returns:
            URL: The updated URL object with incremented clicks.
        """
        
        return self.url_repository.increment_clicks(key)

    def delete_short_url(self, secret_key: str) -> URL | None:
        """Deactivate URL by secret key

        Args:
            secret_key (str): The secret key of the URL to delete.

        Returns:
            (URL | None): The deleted URL object or None if not found.
        """
        
        return self.url_repository.delete_by_secret_key(secret_key)

    def toggle_short_url(self, secret_key: str) -> URL | None:
        """Toggle URL activation state by secret key

        Args:
            secret_key (str): The secret key of the URL to toggle.

        Returns:
            (URL | None): The updated URL object or None if not found.
        """
        
        return self.url_repository.toggle_active_by_secret_key(secret_key)

    def build_short_url_info(self, db_url: URL) -> URLInfo:
        """Build URLInfo response with full URLs

        Args:
            db_url (URL): The database URL object

        Returns:
            URLInfo: The URLInfo response object
        """
        
        base_url = StarletteURL(self.settings.base_url)

        return URLInfo(
            target_url=db_url.target_url,
            is_active=db_url.is_active,
            clicks=db_url.clicks,
            url=str(base_url.replace(path=f"/{db_url.key}")),
            admin_url=str(base_url.replace(path=f"/admin/{db_url.secret_key}")),
        )
