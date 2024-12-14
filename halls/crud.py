from datetime import datetime

from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select, func


from halls.models import Hall


def get_hall_by_id(session: Session, hall_id: int) -> Hall | None:
    statement = select(Hall).where(Hall.id == hall_id)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        return None


def get_all_paginated_halls(session: Session, offset: int = 0, limit: int = 10, Show_current: bool = True) -> list[Hall]:
    statement_size = select(func.count()).select_from(Hall)
    size = session.exec(statement_size).scalar()
    if (limit*offset) >= size:
        return
    statement = select(Hall).limit(limit).offset(limit*offset).order_by(Hall.schedule).where(
        Hall.schedule >= datetime.now()
        if Show_current
        else Hall.schedule
        )
    return session.exec(statement).all()