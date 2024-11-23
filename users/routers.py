from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from dependencies import get_db, get_request_user
from users import crud
from .models import TokenObtain, User
from . import utils


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me")
def get_current_user(user: User = Depends(get_request_user)) -> User:
    return user


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


@router.post("/login")
def login(user_in: TokenObtain, db: Session = Depends(get_db)) -> str:
    user = crud.get_user_by_username(db, user_in.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username")
    if not utils.verify_password(user_in.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = utils.create_jwt_token(
        {
            "username": user_in.username,
            "bars_id": user.bars_id,
        }
    )
    return token


"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InN0cmluZyIsImJhcnNfaWQiOjAsImV4cCI6MTczNDk4ODU5MX0.RK-Ti1BJ4Vy2IMsxEKukwhbS07ESwASH0wggqpqByrw"
