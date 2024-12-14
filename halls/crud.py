from datetime import datetime

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
    statement = select(Hall).order_by(Hall.schedule)
    return session.exec(statement).all()


def get_all_halls_by_datatime(session: Session) -> list[Hall]:
    statement = select(Hall).order_by(Hall.schedule).where(Hall.schedule >= datetime.now())
    return session.exec(statement).all()