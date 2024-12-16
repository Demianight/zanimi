from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from common.dependencies import get_db, get_request_user
from seats import crud
from users.models import User

from .models import SeatCreate, SeatPublic

router = APIRouter(prefix="/seats", tags=["seats"])


@router.get("/{seat_id}")
def get_seat_by_id(seat_id: int, db: Session = Depends(get_db)) -> SeatPublic:
    seat = crud.get_seat_by_id(db, seat_id)
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    return seat  # type: ignore


@router.post("/", status_code=201)
def create_seat(seat: SeatCreate, db: Session = Depends(get_db)):
    return crud.create_seat(db, seat.block_id, seat.row, seat.column)


@router.post("/{seat_id}/book", status_code=201)
def book_seat(
    seat_id: int,
    user: User = Depends(get_request_user),
    db: Session = Depends(get_db),
) -> SeatPublic:
    seat = crud.book_seat(db, seat_id, user)
    if not seat:
        raise HTTPException(
            status_code=400, detail="Seat is already booked or does not exist"
        )
    return seat  # type: ignore


@router.delete("/{seat_id}/cancel_booking", status_code=204)
def cancel_booking(
    seat_id: int,
    db: Session = Depends(get_db),
):
    crud.cancel_booking(db, seat_id)
