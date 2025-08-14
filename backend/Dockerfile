FROM python:3.11-slim

# System deps for psycopg2-binary at runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq5 \
  && rm -rf /var/lib/apt/lists/*

# Force psycopg2 to use TCP host, never Unix sockets
ENV PGHOST=db
ENV PGPORT=5432
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=influenceos

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]