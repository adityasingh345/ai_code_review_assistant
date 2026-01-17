from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth_utils import hash_password, verify_password
from jwt_utils import create_tokens
from database import get_db

router = APIRouter(prefix="/auth")

from pydantic import BaseModel

class AuthRequest(BaseModel):
    email: str
    password: str



@router.post("/signup")
def signup(data: AuthRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email exists")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    db.add(user)
    db.commit()

    return {"message": "User created"}

@router.post("/login")
def login(data: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_tokens({"sub": user.email})
    return {"access_token": token}
