from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    username: str
    bars_id: int
    password: str = Field(exclude=True)


class TokenObtain(SQLModel):
    username: str
    password: str
