from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "ADITYA"
ALGORITHM = "HS256"

def create_tokens(data: dict, expires_minutes=60):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    
    to_encode.update({"exp":expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)