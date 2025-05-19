from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import database


@asynccontextmanager
async def lifespan(life_app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()
