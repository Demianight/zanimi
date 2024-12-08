from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from database import engine
from users import crud, utils
from users.models import User


def get_db():
    try:
        session = Session(engine)
        yield session
    finally:
        session.close()


BearerToken = HTTPBearer()


def get_request_user(
    raw_token: HTTPAuthorizationCredentials = Depends(BearerToken),
    db: Session = Depends(get_db),
) -> User:
    data = utils.decode_access_token(raw_token.credentials)

    if user := crud.get_user_by_username(db, data["username"]):
        return user

    raise HTTPException(status_code=401, detail="Invalid token")
