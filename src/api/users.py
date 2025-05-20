import fastapi

from src.auth import validate_user, get_current_token
from src.repositories.users import UserRepository

router = fastapi.APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
async def get_user_by_id(user_id: int, token: str = fastapi.Depends(get_current_token)):
    if not validate_user(user_id, token):
        raise fastapi.HTTPException(status_code=403, detail='Not authorized')
    user = await UserRepository.get_user_by_id(user_id)
    return {'data': user}


@router.get("")
async def get_users():
    users = await UserRepository.get_users()
    return {'data': users}


@router.delete("/{user_id}")
async def delete_user(user_id: int, token: str = fastapi.Depends(get_current_token)):

    if not validate_user(user_id, token):
        raise fastapi.HTTPException(status_code=403, detail='Not authorized')

    await UserRepository.delete_user(user_id)

    return {"ok": True}

