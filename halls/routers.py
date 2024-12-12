from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from common.dependencies import get_db
from halls import crud

from .models import HallPublic

router = APIRouter(
    prefix="/hall",
    tags=["halls"],
)


@router.get("/")
def get_halls(db: Session = Depends(get_db)) -> list[HallPublic]:
    return crud.get_all_halls(db)


@router.get("/{hall_id}")
def get_hall(hall_id: int, db: Session = Depends(get_db)) -> HallPublic:
    hall = crud.get_hall_by_id(db, hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Hall not found")
    return hall
