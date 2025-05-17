from fastapi import FastAPI, HTTPException
from src.database import database

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(life_app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    try:
        record = await database.fetchone(f"SELECT * FROM users WHERE id='{user_id}'")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="User with this id does not exists")

    return {"data": f"{record}"}


@app.get("/users")
async def get_users():
    try:
        record = await database.fetchmany('SELECT * FROM users')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Something went wrong")
    return {"data": f"{record}"}


@app.post("/users")
async def add_user(login: str, password: str, nickname: str):
    try:
        record = await database.execute(f"INSERT INTO users (login, password_hash, nickname, money) "
                                        f"VALUES ('{login}','{hash(password)}', '{nickname}', '1000')")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="User with this params already exists")

    return {"ok": True}


@app.delete("users/{user_id}")
async def delete_user(user_id: int):
    try:
        record = await database.execute(f"DELETE FROM users WHERE id='{user_id}'")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="User with this id does not exists")

    return {"ok": True}