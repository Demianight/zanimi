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


def get_all_paginated_halls(session: Session, offset: int = 0, limit: int = 10, relevant_only: bool = True) -> list[Hall]:
    if relevant_only:
        statement = select(Hall).limit(limit).offset(offset).order_by(Hall.schedule).where(Hall.schedule >= datetime.now())
    if not relevant_only:
        statement = select(Hall).limit(limit).offset(offset).order_by(Hall.schedule)
    return session.exec(statement).all()