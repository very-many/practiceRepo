from fastapi import FastAPI

from backend.api.routers import router
from backend.container import Container



def create_application() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    container = Container()
    
    database = container.database()
    database.create_tables()

    app = FastAPI(
        title="URL Shortener API",
        description="A simple URL shortener service",
        version="0.4.0",
    )

    app.container = container

    container.wire(
        modules=[
            "backend.api.routers.url.create_short_url",
            "backend.api.routers.url.forward_to_target_url",
            
            "backend.api.routers.admin.toggle_short_url",
            "backend.api.routers.admin.delete_short_url",
            "backend.api.routers.admin.get_short_url_info",
        ]
    )

    app.include_router(router)
    return app


app: FastAPI = create_application()
