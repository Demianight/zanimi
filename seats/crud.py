from typing import Optional
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from seats.models import Seat
from users.models import User


def get_seat_by_id(
    session: Session, block_id: int, row: int, column: int
) -> Seat | None:
    statement = select(Seat).where(
        Seat.block_id == block_id,
        Seat.row == row,
        Seat.column == column,
    )
    try:
        return session.exec(statement).one()
    except NoResultFound:
        return None


def get_seats_by_block_id(session: Session, block_id: int) -> list[Seat]:
    statement = select(Seat).where(Seat.block_id == block_id)
    return session.exec(statement).all()


def create_seat(session: Session, block_id: int, row: int, column: int) -> Seat:
    new_seat = Seat(status="available", block_id=block_id, row=row, column=column)
    session.add(new_seat)
    session.commit()
    session.refresh(new_seat)
    return new_seat


def book_seat(
    seat_id: int,
    user: User,
    session: Session,
) -> Optional[Seat]:
    seat = session.exec(
        select(Seat).where(Seat.id == seat_id, Seat.status == "available")
    ).first()

    if seat:
        seat.booked_by_id = user.id
        seat.status = "booked"
        session.add(seat)
        session.commit()
        session.refresh(seat)
        return seat

    return None


def cancel_booking(seat_id: int, user: User, session: Session) -> Optional[Seat]:
    seat = session.exec(
        select(Seat).where(Seat.id == seat_id, Seat.booked_by_id == user.id)
    ).first()

    if seat:
        seat.booked_by_id = None
        seat.status = "available"
        session.add(seat)
        session.commit()
        session.refresh(seat)
        return seat

    return None
