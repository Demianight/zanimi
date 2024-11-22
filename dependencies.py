from database import engine
from sqlmodel import Session


def get_db():
    try:
        session = Session(engine)
        yield session
    finally:
        session.close()
