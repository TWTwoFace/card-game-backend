from fastapi import FastAPI
from src.database import database

app = FastAPI()


@app.get("/")
def say_hello():
    return {"data": database.execute_query("""SELECT MIN(id) FROM users""")}

