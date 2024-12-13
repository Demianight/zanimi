from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from common.dependencies import get_db
from seats import crud

from .models import SeatPublic, SeatUpdate
from users import crud as user_crud


router = APIRouter(
    prefix="/seats",
    tags=["Seats"]
    )
router.get("/seats{seats_id}", response_model=SeatPublic)
def get_seat(seat_id: int, db: Session = Depends(get_db)) -> SeatPublic:
    if seat := crud.get_seat_by_id(db, seat_id):
        return seat
    raise HTTPException(status_code=404, detail='Seat not found')


router.post("/seats{seat_id}/book{booked_by_id}", response_model=SeatPublic)
def book_seat(seat_id: int, username: str, db: Session = Depends(get_db)) -> SeatUpdate:
    user = user_crud.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    seat = crud.book_seat(session=db, seat_id=seat_id, booked_by_id=user.id)
    if seat is None:
        raise HTTPException(status_code=404, detail="Seat not found or already booked")
    return seat
