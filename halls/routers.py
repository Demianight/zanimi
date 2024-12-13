from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from common.dependencies import get_db
from halls import crud

from .models import HallPublic, HallPublicWithBlocks

router = APIRouter(
    prefix="/halls",
    tags=["halls"],
)


@router.get("/")
def get_halls(db: Session = Depends(get_db)) -> list[HallPublic]:
    return crud.get_all_halls(db)


@router.get("/{hall_id}")
def get_hall(hall_id: int, db: Session = Depends(get_db)) -> HallPublicWithBlocks:
    if hall := crud.get_hall_by_id(db, hall_id):
        return hall
    raise HTTPException(status_code=404, detail="Hall not found")
