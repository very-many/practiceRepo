import requests

AZURE_KEY = "YOUR_AZURE_KEY_HERE"
AZURE_ENDPOINT = "YOUR_AZURE_ENDPOINT_HERE"

def analyze_image(img_url: str):
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/json",
    }
    body = {"url": img_url}
    api_url = f"{AZURE_ENDPOINT}/face/v1.0/detect?detectionModel=detection_01&returnFaceRectangle=true"
    response = requests.post(api_url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()