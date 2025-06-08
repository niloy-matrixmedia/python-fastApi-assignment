from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, UserUpdate
from app.models.user import User
from app.utils.security import hash_password, verify_password, create_access_token
from app.core.database import get_db


def register_user(user: UserCreate, db: Session):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        bio=user.bio
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(user: UserLogin, db: Session):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token({"sub": str(db_user.id)}), "token_type": "bearer"}

def update_profile(current_user: User, user_update: UserUpdate, db: Session):
    if user_update.name:
        current_user.name = user_update.name
    if user_update.bio:
        current_user.bio = user_update.bio
    db.commit()
    db.refresh(current_user)
    return current_user

def delete_user(current_user: User, db: Session):
    current_user.is_active = False
    db.commit()