from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import auth, posts
from .db import wait_for_db

app = FastAPI(title="InfluenceOS Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wait for DB at startup so first requests don’t fail
@app.on_event("startup")
def _startup() -> None:
    wait_for_db()

app.include_router(auth.router, prefix="/auth")
app.include_router(posts.router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}