from dependency_injector import containers, providers
from backend.database.database import Database
from backend.services.url_service import URLService
from backend.services.key_service import KeyService
from backend.database.url_repository import URLRepository
from backend.config import get_settings

class Container(containers.DeclarativeContainer):
    """Dependency injection container for the application.

    Attributes:
        config (Configuration): Application configuration.
        database (Database): Singleton Database instance.
        key_service (KeyService): Key management service.
        url_service (URLService): URL shortening service.
    """
    
    # Configuration
    settings = providers.Singleton(get_settings)

    # Database
    database = providers.Singleton(Database, db_url=settings.provided.db_url)
    
    # Session Factory - provides a callable that returns new sessions
    session_factory = providers.Factory(
        lambda db: db._session_factory,
        db=database
    )

    # Services
    key_service = providers.Factory(KeyService, session_factory=session_factory)

    url_repository = providers.Factory(URLRepository, session_factory=session_factory)
    
    url_service = providers.Factory(
        URLService, url_repository=url_repository, key_service=key_service, settings=settings
    )
