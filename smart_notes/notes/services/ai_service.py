import requests
from django.conf import settings

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

def summarize_text(text: str) -> str:
    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"
    }

    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 130,
            "min_length": 30,
            "do_sample": False
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        if response.status_code == 503:
            raise Exception("Model is loading. Try again in a few seconds.")

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list) and "summary_text" in data[0]:
            return data[0]["summary_text"]

        if isinstance(data, dict) and "error" in data:
            raise Exception(f"API Error: {data['error']}")

        raise Exception("Unexpected API response format")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")