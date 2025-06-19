from fastapi import APIRouter, HTTPException
import jwt
from sqlalchemy.orm import Session
from fastapi import Depends

from app import auth, auth0, crud
from . import models, schemas
from .database import SessionLocal
import jwt as pyjwt

router = APIRouter()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def identify_token_type(token: str):
    try:
        un = pyjwt.decode(token, options={"verify_signature": False})
        return "auth0" if un.get("iss", "").startswith("https://") else "local"
    except Exception:
        raise HTTPException(401, "Invalid token format")

def decode_token(token: str):
    typ = identify_token_type(token)
    if typ == "local":
        try:
            return pyjwt.decode(token, auth.AUTHOR_SECRET_KEY, algorithms=["HS256"])
        except pyjwt.PyJWTError:
            raise HTTPException(401, "Invalid local token")
    else:
        return auth0.verify_auth0_token(token)

@app.post("/api/users/get-user-data", response_model=schemas.UserDataResponse)
def get_user_data(request: schemas.UserDataRequest, db: Session = Depends(auth.get_db)):
    payload = decode_token(request.token)
    email = payload.get("email") or payload.get("sub")
    user = crud.get_user_by_email(db, email)
    if not user:
        user = crud.create_user(db, payload.get("name", email), email, "", auth_type="auth0")
    return schemas.UserDataResponse(id=user.id, fullName=user.full_name, email=user.email)