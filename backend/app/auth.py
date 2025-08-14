from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import os
import httpx

router = APIRouter()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8000/auth/callback")

if not CLIENT_ID or not CLIENT_SECRET:
    raise RuntimeError("LinkedIn CLIENT_ID/CLIENT_SECRET not configured.")

# Demo in-memory token store
token_store = {}

@router.get("/login")
async def linkedin_login():
    scopes = "profile%20email%20openid%20w_member_social"
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&scope={scopes}"
    )
    return RedirectResponse(auth_url)

@router.get("/callback")
async def linkedin_callback(code: str | None = None):
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code.")

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(token_url, data=payload, timeout=30)
        resp.raise_for_status()
        token_data = resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=500, detail=f"No access_token in response: {token_data}")
        token_store["access_token"] = access_token
        return RedirectResponse(url="http://localhost:3000/")