from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # створює таблицю при старті сервера
    yield


app = FastAPI(title="Auth Service", lifespan=lifespan)
app.include_router(auth.router)
