import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set. Please set it in environment or .env file.")

def generate_post(prompt: str, max_output_tokens: int = 300):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": max_output_tokens
        }
    }
    resp = requests.post(url, json=data, headers=headers, timeout=30)
    resp.raise_for_status()
    r = resp.json()

    # Show the response if the structure is unexpected
    if "candidates" not in r:
        raise RuntimeError(f"API returned unexpected response: {r}")

    return r["candidates"][0]["content"]["parts"][0]["text"]

if __name__ == "__main__":
    print(generate_post("Write me a short LinkedIn post about AI ethics."))
