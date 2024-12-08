from datetime import datetime
from typing import Annotated, Optional

from annotated_types import Ge
from sqlmodel import Field, Relationship, SQLModel


class Hall(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    schedule: datetime


class Block(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    number: Annotated[int, Ge(1)]
    rows: int
    columns: int

    hall_id: int = Field(foreign_key="hall.id")
    hall: "Hall" = Relationship(back_populates="blocks")
