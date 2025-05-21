from fastapi import APIRouter, Depends, HTTPException

from src.auth import validate_token, get_current_user_id
from src.repositories.matchmaking import MatchmakingRepository


router = APIRouter(prefix='/matchmaking', tags=['Matchmaking'])


@router.get('')
async def get_all_rooms(token: str = Depends(validate_token)):
    rooms = await MatchmakingRepository.get_all_rooms()

    if rooms is None:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'data': rooms}


@router.post('')
async def create_room(user_id: int = Depends(get_current_user_id)):
    room = await MatchmakingRepository.create_room(user_id)

    if room is None:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'ok': True, 'data': room}


@router.patch('/{room_id}')
async def join_room(room_id: int, user_id: int = Depends(get_current_user_id)):
    result = await MatchmakingRepository.join_room(room_id, user_id)

    if not result:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'ok': True}


@router.delete('')
async def delete_room(user_id: int = Depends(get_current_user_id)):
    result = await MatchmakingRepository.delete_room(user_id)

    if not result:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'ok': True}


@router.get('/active')
async def get_active_rooms(user_id: int = Depends(get_current_user_id)):
    result = await MatchmakingRepository.get_active_room(user_id)

    return {'result': result}

