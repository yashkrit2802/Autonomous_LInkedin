# posts.py

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .llm import generate_post
from .linkedin import get_user_urn, post_to_linkedin
from .db import SessionLocal
from .models import User

router = APIRouter()

class GenerateRequest(BaseModel):
    topic: str
    tone: str = "professional"

@router.post("/generate-post")
async def generate_post_endpoint(req: GenerateRequest):
    """
    Generates a draft LinkedIn post.
    """
    prompt = f"Write a LinkedIn post about: {req.topic}. Tone: {req.tone}. Include a hook, 3 takeaways, 3 hashtags. Max 250 words."
    content = generate_post(prompt)
    return {"draft": content}

@router.post("/publish-post")
async def publish_post_endpoint(req: GenerateRequest):
    """
    Generates a post and immediately publishes it to the user's LinkedIn profile.
    """
    session: Session = SessionLocal()
    try:
        # For this example, we fetch the first user. In a real app, you'd use a user ID from the request.
        user = session.query(User).first()
        if not user:
            raise HTTPException(status_code=404, detail="No user found. Please login first.")

        # 1. Generate the post content
        prompt = f"Write a LinkedIn post about: {req.topic}. Tone: {req.tone}. Include a hook, 3 takeaways, 3 hashtags. Max 250 words."
        content = generate_post(prompt)

        # 2. Get the user's LinkedIn URN and access token from the database
        access_token = user.access_token
        user_urn = user.linkedin_urn

        # 3. Publish the post to LinkedIn
        post_response = await post_to_linkedin(access_token, user_urn, content)

        return {"status": "success", "message": "Post published successfully.", "linkedin_response": post_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()