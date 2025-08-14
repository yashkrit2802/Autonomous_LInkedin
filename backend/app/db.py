from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os
import time
import psycopg2


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@db:5432/influenceos",
)

# pool_pre_ping makes stale connections auto-recover
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def wait_for_db(max_tries: int = 120, delay_seconds: float = 1.0) -> None:
    last_err = None
    for _ in range(max_tries):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB", "influenceos"),
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "postgres"),
                host=os.getenv("POSTGRES_HOST", "db"),
                port=int(os.getenv("POSTGRES_PORT", "5432"))
            )
            conn.close()
            return
        except OperationalError as e:
            last_err = e
            time.sleep(delay_seconds)
    raise RuntimeError(f"Database not ready after {max_tries} attempts: {last_err}")