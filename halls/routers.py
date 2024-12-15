from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session

from common.dependencies import get_db
from halls import crud

from .models import HallPublic, HallPublicWithBlocks

router = APIRouter(
    prefix="/halls",
    tags=["halls"],
)


@router.get("/")
def get_halls(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    relevant_only: bool = True,
    minutes: int = Query(default=15, ge=0),
    db: Session = Depends(get_db),
) -> list[HallPublic]:
    if hall := crud.get_all_paginated_halls(db, offset, limit, relevant_only, minutes):
        return hall
    raise HTTPException(status_code=404, detail="No items found.")


@router.get("/{hall_id}")
def get_hall(hall_id: int, db: Session = Depends(get_db)) -> HallPublicWithBlocks:
    if hall := crud.get_hall_by_id(db, hall_id):
        return hall
    raise HTTPException(status_code=404, detail="Hall not found")
