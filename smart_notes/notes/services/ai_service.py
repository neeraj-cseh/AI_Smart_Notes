import requests
from django.conf import settings

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"


def summarize_text(text: str) -> str:
    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"
    }

    payload = {
        "inputs": text
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 503:
        raise Exception("Model is loading. Try again.")

    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):
        return data[0]["summary_text"]

    if "error" in data:
        raise Exception(data["error"])

    raise Exception("Unknown API response")