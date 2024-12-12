from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from halls.models import Hall


def get_hall_by_id(session: Session, hall_id: int) -> Hall | None:
    statement = select(Hall).where(Hall.id == hall_id)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        return None


def get_all_halls(session: Session) -> list[Hall]:
    statement = select(Hall)
    return session.exec(statement).all()
