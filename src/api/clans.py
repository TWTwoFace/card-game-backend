from fastapi import APIRouter, Depends, HTTPException

from src.auth import get_current_user_id
from src.models.clans import ClanCreatingScheme, ClanChangeScheme
from src.repositories.clans import ClanRepository

router = APIRouter(prefix='/clans', tags=['Clans'])


@router.post('')
async def create_clan(clan: ClanCreatingScheme, owner_id: int = Depends(get_current_user_id)):
    result = await ClanRepository.create_clan(owner_id, clan)

    if not result:
        raise HTTPException(status_code=400, detail='Invalid request data')

    return {'ok': True}


@router.patch('')
async def change_clan(clan: ClanChangeScheme, owner_id: int = Depends(get_current_user_id)):
    avatar = False
    description = False

    if clan.avatar is not None:
        avatar = await ClanRepository.change_avatar(owner_id, clan)

    if clan.description is not None:
        description = await ClanRepository.change_description(owner_id, clan)

    if not avatar and not description:
        raise HTTPException(status_code=422, detail='Invalid request data')

    return {
        'result':
            {
                'avatar': avatar,
                'description': description
            }
    }


@router.get('')
async def get_clans():
    clans = await ClanRepository.get_clans()

    if clans is None:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'data': clans}


@router.get('/{clan_id}')
async def get_clan_by_id(clan_id: int):
    clan = await ClanRepository.get_clan_by_id(clan_id)

    if clan is None:
        raise HTTPException(status_code=400, detail='Clan with this id does not exist')

    return {'data': clan}


@router.delete('')
async def delete_clan(owner_id: int = Depends(get_current_user_id)):
    result = await ClanRepository.delete_clan(owner_id)

    if not result:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'ok': True}