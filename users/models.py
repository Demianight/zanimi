from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from seats.models import Seat


# Base class for shared fields
class UserBase(SQLModel):
    username: str


# Main User model with table support
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str = Field(
        exclude=True
    )  # This field is excluded from serialization

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


class TokenObtain(SQLModel):
    username: str
    password: str
