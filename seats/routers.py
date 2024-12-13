from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from common.dependencies import get_db, get_request_user
from seats import crud
from users.models import User

from .models import SeatPublic


router = APIRouter(prefix="/seats", tags=["seats"])


@router.get("/{seats_id}")
def get_seat(
    block_id: int, row: int, column: int, db: Session = Depends(get_db)
) -> SeatPublic:
    seat = crud.get_seat_by_id(db, block_id, row, column)
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    return seat


@router.post("/", status_code=201)
def create_seat(block_id: int, row: int, column: int, db: Session = Depends(get_db)):
    seat = crud.get_seat_by_id(db, block_id, row, column)
    if seat:
        raise HTTPException(status_code=400, detail="Seat already exists")
    return crud.create_seat(db, block_id, row, column)


@router.post("/book{seat_id}", status_code=201)
def book_seat(
    seat_id: int, user: User = Depends(get_request_user), db: Session = Depends(get_db)
) -> SeatPublic:
    seat = crud.book_seat(seat_id, user, db)
    if not seat:
        raise HTTPException(
            status_code=400, detail="Seat is already booked or does not exist"
        )
    return seat


@router.delete("/cancel_booking{seats_id}", status_code=204)
def cancel_booking(
    seat_id: int, user: User = Depends(get_request_user), db: Session = Depends(get_db)
):
    crud.cancel_booking(seat_id, user, db)
    return "Booking was succesfully canceled"
