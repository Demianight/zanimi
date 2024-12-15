from datetime import datetime, timedelta

from sqlmodel import Session, SQLModel, create_engine

from common.utils import create_hall

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


def create_db_and_tables():
    from halls.models import Block, Hall  # noqa
    from seats.models import Seat  # noqa
    from users.models import User  # noqa

    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()

    with Session(engine) as session:
        next_lesson = timedelta(minutes=95 + 15)

        date = datetime(2024, 12, 17, 9, 20)
        create_hall(
            session=session,
            name="Б-201",
            subject="Физика",
            schedule=date,
        )
        date = date + next_lesson
        create_hall(
            session=session,
            name="В-301",
            subject="Программирование",
            schedule=date,
        )
        date = date + 2 * next_lesson
        create_hall(
            session=session,
            name="Ж-401",
            subject="История",
            schedule=date,
        )
