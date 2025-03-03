import requests

# Set your Together AI API key
API_KEY = "tgp_v1__RIq1Lo4_SEpcnMnCLOhbQv8Uajg_7X3dUaM2fXrHUY"

# Define the API endpoint
url = "https://api.together.xyz/inference" 

# Sample payload
payload = {
    "model": "meta-llama/Llama-3-8b-chat-hf",  # Ensure you're using a valid model
    "messages": [{"role": "user", "content": "Hello, how are you?"}],
    "max_tokens": 50
}

# Headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Make the API request
try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error for HTTP errors
    print("API is working fine. Response:")
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")