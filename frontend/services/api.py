import requests
from frontend.config import get_settings


BACKEND_URL = get_settings().base_url


def create_short_url(url: str) -> str:
    headers = {
        "Content-Type": "application/json",
    }
    body = {"target_url": url}
    api_url = f"{BACKEND_URL}/url"
    response = requests.post(api_url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()

def get_admin_info(admin_key: str) -> str:
    headers = {
        "Content-Type": "application/json",
    }
    api_url = f"{BACKEND_URL}/admin/{admin_key}"
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()

def delete_short_url(secret_key: str) -> None:
    headers = {
        "Content-Type": "application/json",
    }
    api_url = f"{BACKEND_URL}/admin/{secret_key}/"
    response = requests.delete(api_url, headers=headers)
    response.raise_for_status()
    

def toggle_short_url(secret_key: str) -> None:
    headers = {
        "Content-Type": "application/json",
    }
    api_url = f"{BACKEND_URL}/admin/{secret_key}/is_active"
    response = requests.put(api_url, headers=headers)
    response.raise_for_status()
