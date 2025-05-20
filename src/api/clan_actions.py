from fastapi import APIRouter, Depends, HTTPException

from src.auth import get_current_user_id
from src.models.clans import ClanActionCreationSchema
from src.repositories.clans import ClanRepository

router = APIRouter(prefix='/clans', tags=['Clan actions'])


@router.post('/clan_actions')
async def create_clan_action(action: ClanActionCreationSchema, user_id: int = Depends(get_current_user_id)):
    result = await ClanRepository.create_clan_action(user_id, action)

    if not result:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'ok': True}


@router.get('/{clan_id}/clan_actions')
async def get_clan_actions(clan_id: int):
    actions = await ClanRepository.get_clan_actions(clan_id)

    if actions is None:
        return HTTPException(status_code=400, detail='Bad request')

    return {'data': actions}
