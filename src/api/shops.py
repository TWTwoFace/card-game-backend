from fastapi import APIRouter, HTTPException, Depends

from src.auth import get_current_user_id
from src.repositories.shops import ShopRepository

router = APIRouter(prefix='/shop', tags=['Shop'])


@router.get('')
async def get_last_shop():
    shop = await ShopRepository.get_last_shop()

    if shop is None:
        raise HTTPException(status_code=404, detail='Last shop does not founded')

    return {'data': shop}


@router.post('/buy')
async def buy_card(sell_item_id: int, user_id: int = Depends(get_current_user_id)):
    result = await ShopRepository.buy_card(user_id, sell_item_id)

    if not result:
        raise HTTPException(status_code=403, detail='Permission denied')

    return {'ok': True}

