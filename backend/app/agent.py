from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from .llm import generate_post  # Your existing LLM module
from .models import User, ContentCalendar
from .db import SessionLocal
import datetime


# ---------------------------
# Agent State Definition
# ---------------------------
class AgentState(TypedDict):
    user_id: int
    topic: str
    research_summary: str
    post_draft: str


# ---------------------------
# Node 1: Choose Topic
# ---------------------------
def choose_topic_node(state: AgentState):
    session = SessionLocal()
    user = session.query(User).filter_by(id=state['user_id']).first()
    today = datetime.date.today()

    # Check if a post is already scheduled today
    scheduled_post = session.query(ContentCalendar).filter(
        ContentCalendar.user_id == user.id,
        ContentCalendar.scheduled_at >= today,
        ContentCalendar.scheduled_at < today + datetime.timedelta(days=1)
    ).first()

    if scheduled_post:
        print("Post already scheduled for today. Exiting.")
        return {"topic": None}

    # Pick a topic (simplified)
    topic = f"Latest trends in {user.industry}"
    return {"topic": topic}


# ---------------------------
# Node 2: Industry Research
# ---------------------------
def research_node(state: AgentState):
    if not state['topic']:
        return state

    prompt = f"Find and summarize recent trends about {state['topic']}."
    research_summary = generate_post(prompt, max_output_tokens=500)
    return {"research_summary": research_summary}


# ---------------------------
# Node 3: Content Generation
# ---------------------------
def generate_content_node(state: AgentState):
    if not state['research_summary']:
        return state

    prompt = (
        f"Create a LinkedIn post draft. Use this research: {state['research_summary']}. "
        "The tone should be professional. Include 3 key takeaways and 3 hashtags."
    )
    post_draft = generate_post(prompt)
    return {"post_draft": post_draft}


# ---------------------------
# Node 4: Schedule Post
# ---------------------------
def schedule_post_node(state: AgentState):
    if not state['post_draft']:
        return state

    session = SessionLocal()
    new_post = ContentCalendar(
        user_id=state['user_id'],
        post_content=state['post_draft'],
        scheduled_at=datetime.datetime.now()
    )
    session.add(new_post)
    session.commit()
    print(f"Post for user {state['user_id']} scheduled successfully.")
    return state


# ---------------------------
# Build Workflow
# ---------------------------
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("choose_topic", choose_topic_node)
workflow.add_node("research", research_node)
workflow.add_node("generate_content", generate_content_node)
workflow.add_node("schedule_post", schedule_post_node)

# Define entry point
workflow.add_edge(START, "choose_topic")

# Define flow
workflow.add_edge("choose_topic", "research")
workflow.add_edge("research", "generate_content")
workflow.add_edge("generate_content", "schedule_post")
workflow.add_edge("schedule_post", END)

# Compile graph into runnable app
app = workflow.compile()
