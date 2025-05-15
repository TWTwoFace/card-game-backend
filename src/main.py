from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def say_hello():
    return {"data": "hello, world!"}

