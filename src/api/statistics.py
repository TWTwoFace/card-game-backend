from fastapi import APIRouter, HTTPException

from src.repositories.statistics import StatisticsRepository

router = APIRouter(tags=["Statistics"])


@router.get("/users/{user_id}/statistics")
async def get_user_statistics(user_id: int):
    stats = await StatisticsRepository.get_statistics_by_user_id(user_id)

    if stats is None:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'data': stats}

