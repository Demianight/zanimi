from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from halls.models import Block
from users.models import User


class Seat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    row: int
    column: int

    block_id: int = Field(foreign_key="block.id")
    block: "Block" = Relationship(back_populates="heroes")

    booked_by_id: int = Field(foreign_key="user.id", default=None)
    booked_by: Optional["User"] = Relationship(back_populates="seats")
