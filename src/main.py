from fastapi import FastAPI

from src.api import main_router
from src.lifespan import lifespan


app = FastAPI(lifespan=lifespan)

app.include_router(main_router)


