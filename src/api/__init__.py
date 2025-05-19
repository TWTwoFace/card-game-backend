from fastapi import APIRouter

from src.api.users import router as users_router
from src.api.register import router as reg_router
from src.api.login import router as log_router
from src.api.clans import router as clans_router

__all__ = [
    'main_router'
]


main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(reg_router)
main_router.include_router(log_router)
main_router.include_router(clans_router)
