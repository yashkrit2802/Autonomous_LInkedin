# linkedin.py

import os
import httpx

async def get_user_urn(access_token: str):
    """
    Retrieves the unique LinkedIn URN (ID) of the authenticated user.
    This is required for making posts.
    """
    if not access_token:
        raise ValueError("No access token found. Please authenticate.")

    api_url = "https://api.linkedin.com/v2/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers, timeout=30)
        response.raise_for_status()
        user_info = response.json()
        return user_info.get("sub") # 'sub' is the URN in the new API

async def post_to_linkedin(access_token: str, user_urn: str, content: str):
    """
    Publishes a text post to the authenticated user's LinkedIn profile.
    """
    if not access_token:
        raise ValueError("No access token found. Please authenticate.")

    api_url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    payload = {
        "author": f"urn:li:person:{user_urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()