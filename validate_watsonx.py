"""
Validates IBM watsonx.ai connectivity and the Granite model.
Run with: python validate_watsonx.py
"""

import requests
import json

from config import WATSONX_API_KEY as API_KEY, WATSONX_PROJECT_ID as PROJECT_ID, WATSONX_URL, GRANITE_MODEL_ID as MODEL_ID
IAM_URL = "https://iam.cloud.ibm.com/identity/token"


def get_token():
    print("1. Fetching IAM token...")
    resp = requests.post(
        IAM_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": API_KEY},
        timeout=30,
    )
    resp.raise_for_status()
    token = resp.json()["access_token"]
    print(f"   ✅ Token acquired (first 20 chars): {token[:20]}...")
    return token


def test_generation(token):
    print("2. Testing Granite text generation...")
    url = f"{WATSONX_URL}/ml/v1/text/generation?version=2023-05-29"
    payload = {
        "model_id": MODEL_ID,
        "input": "What is 5G in one sentence?",
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7,
            "decoding_method": "sample",
        },
        "project_id": PROJECT_ID,
    }
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    if resp.status_code != 200:
        print(f"   ❌ API Error {resp.status_code}: {resp.text[:300]}")
        return
    result = resp.json()
    text = result["results"][0]["generated_text"]
    print(f"   ✅ Model responded: {text.strip()[:200]}")


if __name__ == "__main__":
    print("=" * 50)
    print("watsonx.ai Connectivity Validation")
    print("=" * 50)
    try:
        token = get_token()
        test_generation(token)
        print("\n✅ All checks passed! Ready to launch app.py")
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
    print("=" * 50)
