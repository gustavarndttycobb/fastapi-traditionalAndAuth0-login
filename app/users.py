from fastapi import APIRouter, HTTPException
import jwt
from sqlalchemy.orm import Session
from fastapi import Depends
from . import models, schemas
from .database import SessionLocal

router = APIRouter()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/users/get-user-data", response_model=schemas.UserDataResponse)
def get_user_data(request: schemas.UserDataRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token verification failed")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return schemas.UserDataResponse(
        id=user.id,
        fullName=user.full_name,
        email=user.email
    )