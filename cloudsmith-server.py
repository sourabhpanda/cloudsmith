from fastapi import FastAPI, Request
import httpx
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Your PAT
REPO = "sourabhpanda/cloudsmith"
EVENT_TYPE = "cloudsmith-webhook"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
print("Loaded token:", GITHUB_TOKEN)  # Debug the token

if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN not found in environment variables.")

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()

    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        data = {
            "event_type": EVENT_TYPE,
            "client_payload": payload
        }
        response = await client.post(
            f"https://api.github.com/repos/{REPO}/dispatches",
            headers=headers,
            json=data
        )

    return {"status": response.status_code}
