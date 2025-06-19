from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app import crud

from .database import SessionLocal
from . import models, schemas

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/api/auth/signup", response_model=schemas.MessageResponse)
def signup(data: schemas.SignupRequest, db: Session = Depends(get_db)):
    crud.get_user_by_email(db, data.email) and HTTPException(400, "Email already registered")
    hashed = pwd_context.hash(data.password)
    crud.create_user(db, data.fullName, data.email, hashed, auth_type="local")
    return {"message": "User created successfully"}

@router.post("/api/auth/login", response_model=schemas.TokenResponse)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, data.email)
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = jwt.encode({"sub": user.email, "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}