from fastapi import APIRouter, Depends, HTTPException

from src.auth import get_current_token, validate_user
from src.repositories.cards import CardRepository

router = APIRouter(tags=['Cards'])


@router.patch('/users/{user_id}/cards/{card_id}')
async def upgrade_card(user_id: int, card_id: int, token: str = Depends(get_current_token)):
    if not validate_user(user_id, token):
        raise HTTPException(status_code=403, detail='Forbidden for user with this user_id')

    result = await CardRepository.upgrade_card(user_id, card_id)

    if not result:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'ok': True}


@router.get('/users/{user_id}/cards')
async def get_user_cards(user_id: int):
    cards = await CardRepository.get_cards_by_user_id(user_id)

    if cards is None:
        raise HTTPException(status_code=400, detail='Bad request')

    return cards






