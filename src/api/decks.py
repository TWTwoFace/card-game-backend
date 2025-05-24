from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field

from src.auth import get_current_token, validate_user
from src.repositories.decks import DeckRepository

router = APIRouter(tags=['Decks'])


@router.post('/users/{user_id}/decks')
async def create_deck(user_id: int, deck_number: Annotated[int, Field(ge=1, le=4)], token: str = Depends(get_current_token)):
    if not validate_user(user_id, token):
        raise HTTPException(status_code=403, detail='Forbidden for user with this user_id')

    result = await DeckRepository.create_deck(user_id, deck_number)

    if not result:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'ok': True}


@router.patch('/users/{user_id}/decks')
async def add_card_to_deck(user_id: int, card_id: int, deck_number: Annotated[int, Field(ge=1, le=4)], token: str = Depends(get_current_token)):
    if not validate_user(user_id, token):
        raise HTTPException(status_code=403, detail='Forbidden for user with this user_id')

    result = await DeckRepository.add_card_to_deck(user_id, card_id, deck_number)

    if not result:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'ok': True}


@router.delete('/users/{user_id}/decks')
async def remove_card_from_deck(user_id: int, card_id: int, token: str = Depends(get_current_token)):
    if not validate_user(user_id, token):
        raise HTTPException(status_code=403, detail='Forbidden for user with this user_id')

    result = await DeckRepository.remove_card_from_deck(user_id, card_id)

    if not result:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'ok': True}


@router.get('/users/{user_id}/decks/{deck_number}')
async def get_deck_cards(user_id: int, deck_number: Annotated[int, Field(ge=1, le=4)], token: str = Depends(get_current_token)):
    if not validate_user(user_id, token):
        raise HTTPException(status_code=403, detail='Forbidden for user with this user_id')

    cards = await DeckRepository.get_user_deck(user_id, deck_number)

    if cards is None:
        raise HTTPException(status_code=400, detail='Bad request')

    return {'data': cards}
