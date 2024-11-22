from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from users.models import User


def create_user(
    session: Session, username: str, password: str, bars_id: int
) -> User:
    new_user = User(username=username, password=password, bars_id=bars_id)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


# Read (get) a single user by ID
def get_user_by_id(session: Session, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        return None


# Read (get) all users
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
        user.password = password
    if bars_id is not None:
        user.bars_id = bars_id

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Delete a user
def delete_user(session: Session, user_id: int) -> bool:
    user = get_user_by_id(session, user_id)
    if not user:
        return False

    session.delete(user)
    session.commit()
    return True
