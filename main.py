from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_db_and_tables
from users.routers import router as user_router
from halls.routers import router as hall_router
from seats.routers import router as seat_router


@asynccontextmanager
async def lifespan(app):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user_router)
app.include_router(hall_router)
app.include_router(seat_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
