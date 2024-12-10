from datetime import datetime
from typing import Annotated, Optional

from annotated_types import Ge
from sqlmodel import Field, Relationship, SQLModel

from seats.models import Seat, SeatPublic


# Base class for Block
class BlockBase(SQLModel):
    number: Annotated[int, Ge(1)]
    rows: int
    columns: int


# Block model with table support
class Block(BlockBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    hall_id: int = Field(foreign_key="hall.id")
    hall: "Hall" = Relationship(back_populates="blocks")

    seats: list[Seat] = Relationship(back_populates="block")


# Block create model
class BlockCreate(BlockBase):
    hall_id: int


# Block update model
class BlockUpdate(SQLModel):
    number: Optional[Annotated[int, Ge(1)]] = None
    rows: Optional[int] = None
    columns: Optional[int] = None


# Block public model
class BlockPublic(BlockBase):
    id: int
    hall_id: int


# Block public model with seats
class BlockPublicWithSeats(BlockPublic):
    seats: list[SeatPublic]


# Base class for Hall
class HallBase(SQLModel):
    name: str
    schedule: datetime


# Hall model with table support
class Hall(HallBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    blocks: list[Block] = Relationship(back_populates="hall")


# Hall create model
class HallCreate(HallBase):
    pass


# Hall update model
class HallUpdate(SQLModel):
    name: Optional[str] = None
    schedule: Optional[datetime] = None


# Hall public model
class HallPublic(HallBase):
    id: int


# Hall public model with blocks
class HallPublicWithBlocks(HallPublic):
    blocks: list["BlockPublicWithSeats"]
