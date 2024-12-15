from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from common.dependencies import get_db, get_request_user
from users import crud

from . import utils
from .models import TokenObtain, User, UserCreate, UserPublic

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me")
def get_current_user(
    user: User = Depends(get_request_user),
) -> UserPublic:
    return user


@router.get("/")
def get_users(db: Session = Depends(get_db)) -> list[UserPublic]:
    return crud.get_all_users(db)


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserPublic:
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserPublic:
    return crud.create_user(db, user.username, user.password)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db, user_id)


@router.post("/login")
def login(user_in: TokenObtain, db: Session = Depends(get_db)) -> str:
    user = crud.get_user_by_username(db, user_in.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username")
    if not utils.verify_password(user_in.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = utils.create_jwt_token({"username": user_in.username})
    return token
