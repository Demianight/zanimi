from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from users.models import User
from users.utils import hash_password


def create_user(
    session: Session, username: str, password: str, bars_id: int
) -> User:
    new_user = User(
        username=username, password=hash_password(password), bars_id=bars_id
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


def get_user_by_id(session: Session, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        return None


def get_user_by_username(session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        return None


def get_all_users(session: Session) -> list[User]:
    statement = select(User)
    return session.exec(statement).all()  # type: ignore


def update_user(
    session: Session,
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    bars_id: int | None = None,
) -> User | None:
    user = get_user_by_id(session, user_id)
    if not user:
        return None

    if username is not None:
        user.username = username
    if password is not None:
        user.password = hash_password(password)
    if bars_id is not None:
        user.bars_id = bars_id

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    user = get_user_by_id(session, user_id)
    if not user:
        return False

    session.delete(user)
    session.commit()
    return True
