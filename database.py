from sqlmodel import SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


def create_db_and_tables():
    from halls.models import Block, Hall  # noqa
    from seats.models import Seat  # noqa
    from users.models import User  # noqa

    SQLModel.metadata.create_all(engine)
