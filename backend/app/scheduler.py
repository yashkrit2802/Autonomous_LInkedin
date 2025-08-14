# scheduler.py (Updated logic)
from apscheduler.schedulers.asyncio import AsyncIOScheduler # Use the async scheduler
from .db import SessionLocal
from .models import User, ContentCalendar
from .linkedin import post_to_linkedin
from .agent import app
import datetime
import asyncio

scheduler = AsyncIOScheduler()

async def run_agent_and_schedule():
    print("Running autonomous agent to generate new content...")
    session = SessionLocal()
    users = session.query(User).all()
    for user in users:
        await app.ainvoke({"user_id": user.id, "topic": None, "research_summary": None, "post_draft": None})
    session.close()

async def publish_scheduled_posts():
    print("Checking for posts to publish...")
    session = SessionLocal()
    posts_to_publish = session.query(ContentCalendar).filter(
        ContentCalendar.scheduled_at <= datetime.datetime.now(),
        ContentCalendar.is_published == False
    ).all()
    
    for post in posts_to_publish:
        user = post.user
        try:
            # Pass the access token from the user object
            await post_to_linkedin(user.access_token, user.linkedin_urn, post.post_content)
            
            post.is_published = True
            session.commit()
            print(f"Post {post.id} published successfully.")
        except Exception as e:
            print(f"Failed to publish post {post.id}: {e}")
    session.close()

def start_scheduler():
    scheduler.add_job(run_agent_and_schedule, 'cron', hour=8, minute=0) # Run agent every day at 8 AM
    scheduler.add_job(publish_scheduled_posts, 'interval', minutes=15)
    scheduler.start()