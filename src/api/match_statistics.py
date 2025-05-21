from fastapi import APIRouter, Depends, HTTPException

from src.auth import get_current_token, validate_user
from src.repositories.match_statistics import MatchStatisticsRepository


router = APIRouter(prefix='/matches', tags=['Matches'])


@router.get('/{user_id}')
async def get_user_matches(user_id: int, token: str = Depends(get_current_token)):
    if not validate_user(user_id, token):
        raise HTTPException(status_code=403, detail='Forbidden for user with this user_id')

    matches = await MatchStatisticsRepository.get_users_matches(user_id)

    if matches is None:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'data': matches}
