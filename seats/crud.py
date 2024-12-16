from typing import Optional, Sequence

from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from seats.exceptions import AlreadyBookedException
from seats.models import Seat
from users.models import User


def get_seat_by_id(session: Session, seat_id: int) -> Optional[Seat]:
    statement = select(Seat).where(Seat.id == seat_id)
    try:
        return session.exec(statement).one()
    except NoResultFound:
        return None


def get_seats_by_block_id(session: Session, block_id: int) -> Sequence[Seat]:
    statement = select(Seat).where(Seat.block_id == block_id)
    return session.exec(statement).all()


def create_seat(
    session: Session,
    block_id: int,
    row: int,
    column: int,
    status: str = "available",
) -> Seat:
    new_seat = Seat(status=status, block_id=block_id, row=row, column=column)
    session.add(new_seat)
    session.commit()
    session.refresh(new_seat)
    return new_seat


def book_seat(
    session: Session,
    seat_id: int,
    user: User,
) -> Optional[Seat]:
    statement = select(Seat).where(
        Seat.id == seat_id, Seat.status == "available"
    )
    seat = session.exec(statement).first()

    if not seat:
        return None

    if seat.block.hall.id in [seat.block.hall.id for seat in user.seats]:
        raise AlreadyBookedException

    seat.booked_by_id = user.id
    seat.status = "booked"
    session.add(seat)
    session.commit()
    session.refresh(seat)
    return seat


def cancel_booking(
    session: Session,
    seat_id: int,
) -> Optional[Seat]:
    statement = select(Seat).where(Seat.id == seat_id)
    seat = session.exec(statement).first()

    if not seat:
        return None

    seat.booked_by_id = None
    seat.status = "available"
    session.add(seat)
    session.commit()
    session.refresh(seat)
    return seat
