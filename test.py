from backend.app.agent import app

# Mock state to pass into workflow
initial_state = {
    "user_id": 1,
    "topic": "",
    "research_summary": "",
    "post_draft": ""
}

# Monkeypatch for local testing (skip DB + real LLM)
import agent

agent.SessionLocal = lambda: None  # Fake DB session
agent.User = type("User", (), {"id": 1, "industry": "Artificial Intelligence"})
agent.ContentCalendar = type(
    "ContentCalendar",
    (),
    {"user_id": None, "post_content": None, "scheduled_at": None}
)
agent.generate_post = lambda prompt, max_output_tokens=500: f"[FAKE OUTPUT for prompt: {prompt}]"

# Fake choose_topic_node that doesn't require DB
def fake_choose_topic_node(state):
    return {"topic": "AI Trends 2025"}

agent.choose_topic_node = fake_choose_topic_node

# Run the workflow
final_state = app.invoke(initial_state)

print("\n--- FINAL STATE ---")
print(final_state)
