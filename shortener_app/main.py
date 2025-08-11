from fastapi import FastAPI
from .api.routers import url, admin
from .database import engine
from .models.url import URL as url_models

url_models.metadata.create_all(bind=engine)

def create_application() -> FastAPI:
    app = FastAPI(
        title="URL Shortener API",
        description="A simple URL shortener service",
        version="0.4.0",
    )

    # Include routers
    app.include_router(url.router)
    app.include_router(admin.router)

    return app


app = create_application()


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "healthy", "message": "URL Shortener API is running"}
