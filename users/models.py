from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from seats.models import Seat, SeatPublic


# Base class for shared fields
class UserBase(SQLModel):
    username: str


# Main User model with table support
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    seats: list[Seat] = Relationship(back_populates="booked_by")


# User create model
class UserCreate(UserBase):
    password: str  # Required for creating a user


# User update model
class UserUpdate(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None


# User public model
class UserPublic(UserBase):
    id: int
    seats: list[SeatPublic]


class TokenObtain(SQLModel):
    username: str
    password: str
