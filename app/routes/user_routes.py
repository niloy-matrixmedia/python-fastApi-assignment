from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserLogin, UserUpdate, UserOut
from app.controllers.user_controller import register_user, login_user, update_profile, delete_user
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return login_user(user, db)

@router.put("/profile", response_model=UserOut)
def profile_update(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_profile(current_user, user_update, db)

@router.delete("/user")
def soft_delete(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    delete_user(current_user, db)
    return {"msg": "User deactivated"}