from datetime import datetime

from sqlalchemy.orm import Session

from halls.models import Block, Hall
from seats.models import Seat


def create_hall(
    session: Session,
    name: str,
    subject: str,
    schedule: datetime,
    blocks_info: list[dict[str, int]] | None = None,
):
    if blocks_info is None:
        blocks_info = []
    hall = Hall(name=name, subject=subject, schedule=schedule)
    session.add(hall)
    session.commit()
    session.refresh(hall)

    for block_info in blocks_info:
        block = Block(hall_id=hall.id, **block_info)
        session.add(block)
        session.commit()
        session.refresh(block)
        for row in range(block_info["rows"]):
            for column in range(block_info["columns"]):
                seat = Seat(
                    status="available",
                    block_id=block.id,
                    row=row,
                    column=column,
                )
                session.add(seat)

    session.commit()
