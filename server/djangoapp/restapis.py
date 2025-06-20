import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load URLs from .env
backend_url = os.getenv('backend_url', default="http://localhost:3030").rstrip("/")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/").rstrip("/") + "/"

# ✅ Function to call backend GET endpoints
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
    request_url = f"{backend_url}/{endpoint}"
    if params:
        request_url += f"?{params.rstrip('&')}"
    
    print("GET from:", request_url)
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Network exception occurred:", e)
        return None

# ✅ Function to call sentiment analyzer
def analyze_review_sentiments(text):
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    print("Analyzing sentiment at:", request_url)
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        result = response.json()
        return result.get("label", "neutral")
    except Exception as e:
        print("Sentiment analysis failed:", e)
        return "neutral"

# ✅ Function to POST review to backend
def post_review(data_dict):
    request_url = f"{backend_url}/review"
    print("POST to:", request_url)
    try:
        response = requests.post(
            request_url,
            json=data_dict,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("POST review failed:", e)
        return None
