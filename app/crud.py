from sqlalchemy.orm import Session
from . import models

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, full_name, email, hashed_password, auth_type="local"):
    user = models.User(full_name=full_name, email=email, hashed_password=hashed_password or "", auth_type=auth_type)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
