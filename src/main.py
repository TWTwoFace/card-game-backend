from fastapi import FastAPI
from src.database import database

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(life_app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/first_user")
async def get_first_user():
    record = await database.fetchone('SELECT * FROM users')
    return {"data": f"{record}"}


@app.get("/user_min_id")
async def get_user_min_id():
    record = await database.fetchone('SELECT MIN(id) FROM users')
    return {"data": f"{record['min']}"}
