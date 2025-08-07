import requests


BACKEND_URL = "http://localhost:8000"


def create_url(url: str) -> str:
    headers = {
        "Content-Type": "application/json",
    }
    body = {"target_url": url}
    api_url = f"{BACKEND_URL}/url"
    response = requests.post(api_url, headers=headers, json=body)
    response.raise_for_status()
    return response.json().get("url", "")
