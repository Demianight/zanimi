from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_db_and_tables
from users.routers import router as user_router


@asynccontextmanager
async def lifespan(app):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
