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
            blocks_info=[
                {"rows": 14, "columns": 6, "number": 1},
                {"rows": 13, "columns": 8, "number": 2},
                {"rows": 13, "columns": 8, "number": 3},
                {"rows": 14, "columns": 6, "number": 4},
            ],
        )
        date = date + next_lesson
        create_hall(
            session=session,
            name="В-301",
            subject="Программирование",
            schedule=date,
            blocks_info=[
                {"rows": 10, "columns": 8, "number": 1},
                {"rows": 11, "columns": 7, "number": 2},
                {"rows": 11, "columns": 7, "number": 3},
                {"rows": 10, "columns": 8, "number": 4},
            ],
        )
        date = date + 2 * next_lesson
        create_hall(
            session=session,
            name="Ж-401",
            subject="История",
            schedule=date,
            blocks_info=[
                {"rows": 8, "columns": 6, "number": 1},
                {"rows": 12, "columns": 6, "number": 2},
                {"rows": 12, "columns": 6, "number": 3},
                {"rows": 8, "columns": 6, "number": 4},
            ],
        )
