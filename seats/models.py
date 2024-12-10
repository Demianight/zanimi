from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from halls.models import Block
    from users.models import User


# Base class for Seat
class SeatBase(SQLModel):
    row: int
    column: int
    block_id: int
    booked_by_id: Optional[int] = None


# Seat model with table support
class Seat(SeatBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    block_id: int = Field(foreign_key="block.id")
    booked_by_id: Optional[int] = Field(default=None, foreign_key="user.id")

    block: "Block" = Relationship(back_populates="seats")
    booked_by: Optional["User"] = Relationship(back_populates="seats")


# Seat create model
class SeatCreate(SeatBase):
    pass


# Seat update model
class SeatUpdate(SQLModel):
    row: Optional[int] = None
    column: Optional[int] = None
    block_id: Optional[int] = None
    booked_by_id: Optional[int] = None


# Seat public model
class SeatPublic(SeatBase):
    id: int
