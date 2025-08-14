# Influence OS — Starter Skeleton

## Prereqs
- Docker & Docker Compose
- An OpenAI API key (put in `.env`)

## Run
1. Copy `.env.example` -> `.env` and fill values.
2. `docker-compose up --build`
3. Backend at http://localhost:8000
4. Frontend at http://localhost:3000

## Next steps
- Implement full DB models and migrations (Alembic).
- Implement real LinkedIn token exchange in `/auth/callback`.
- Add Redis + Celery for scheduling background publishing jobs.
- Add user sessions & secure token storage.
- Expand LLM prompts and safety checks.
