import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/42f35fba38066103e3c145cf0b96bb25/ai/run/"
headers = {"Authorization": f"Bearer {os.getenv("API_KEY")}"}


def generate_text(prompt):
    inputs = [
    { "role": "user", "content": prompt}
    ]
    input = { "messages": inputs }
    model = "@cf/meta/llama-3-8b-instruct"
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()["result"]["response"]