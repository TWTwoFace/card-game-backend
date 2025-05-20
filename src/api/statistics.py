from fastapi import APIRouter, HTTPException

from src.repositories.statistics import StatisticsRepository
from src.repositories.users import UserRepository

router = APIRouter(tags=["Statistics"])


@router.get("/users/{user_id}/statistics")
async def get_user_statistics(user_id: int):
    stats = await StatisticsRepository.get_statistics_by_user_id(user_id)

    if stats is None:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'data': stats}


@router.get('/statistics/top')
async def get_top_users():
    top = await UserRepository.get_top_users(100)

    if top is None:
        raise HTTPException(status_code=400, detail='Bad request')
    return {'data': top}