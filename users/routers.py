from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from dependencies import get_db
from users import crud
from .models import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
def get_users(db: Session = Depends(get_db)) -> list[User]:
    return crud.get_all_users(db)


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/")
def create_user(user: User, db: Session = Depends(get_db)):
    return crud.create_user(db, user.username, user.password, user.bars_id)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)
