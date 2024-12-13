from typing import Optional
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from seats.models import Seat


def get_seat_by_id(session: Session, seat_id: int) -> Seat | None:
    statement = select(Seat).where(Seat.id == seat_id)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        return None
    

def get_all_seats(session: Session) -> list[Seat]:
    statement = select(Seat)
    return session.exec(statement).all()


def book_seat(seat_id: int, booked_by_id: int, session: Session) -> Optional[Seat]:
    seat = get_seat_by_id(session, seat_id)
    if seat and seat.status == "avaliable":
        seat.status = "booked"
        seat.booked_by_id = booked_by_id
        session.commit()
        session.refresh(seat)
        return seat
    return None

