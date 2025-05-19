from fastapi import APIRouter, HTTPException

from src.auth import create_token
from src.models.users import UserLoginSchema
from src.repositories.users import UserRepository

router = APIRouter(prefix='/login')


@router.post('')
async def login(user: UserLoginSchema):
    logged_user = await UserRepository.login_user(user)

    if logged_user is not None and logged_user.login == user.login:
        data = {"id": logged_user.id, "nickname": logged_user.nickname, "money": logged_user.money}
        access_token = create_token(data)
        return {"ok": True, "access_token": access_token, "user": logged_user}
    else:
        raise HTTPException(status_code=401, detail="Incorrect login or password")
