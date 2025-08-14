# backend/app/security.py
import os
import jwt
from datetime import datetime, timedelta
from jwt import ExpiredSignatureError, InvalidTokenError

# Secret & algorithm
SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret_key")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

def create_session_token(linkedin_id: str):
    """
    Create a signed JWT token for the given LinkedIn user ID.
    """
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": linkedin_id,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_session_token(token: str):
    """
    Decode and validate a JWT token, returning the payload.
    Raises jwt.ExpiredSignatureError if expired,
    or jwt.InvalidTokenError if invalid.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
