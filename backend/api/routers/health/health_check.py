from fastapi import APIRouter

router = APIRouter(
    tags=["Health"],
)


@router.get("/", tags=["Health"])
def health_check() -> dict:
    """Health check endpoint.

    Returns:
        dict: A dictionary containing the status and message of the API.
            - status (str): The health status ("healthy").
            - message (str): A descriptive message about the API status.
    """
    
    return {"status": "healthy", "message": "URL Shortener API is running"}
