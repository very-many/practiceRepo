from fastapi import HTTPException, Request

def raise_bad_request(message: str):
    """Raises an HTTP 400 error for bad requests.

    Args:
        message (str): The error message to include in the response.

    Raises:
        HTTPException: 400 Bad Request error.
    """
    raise HTTPException(status_code=400, detail=message)


def raise_not_found(request: Request):
    """Raises an HTTP 404 error for not found resources.

    Args:
        request (Request): The FastAPI request object.

    Raises:
        HTTPException: 404 Not Found error.
    """
    message: str = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)
