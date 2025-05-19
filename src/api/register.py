from fastapi import APIRouter

from src.models.users import UserRegisterSchema
from src.repositories.users import UserRepository

router = APIRouter(prefix='/register', tags=["Registration"])


@router.post("")
async def register_user(user: UserRegisterSchema):
    await UserRepository.create_user(user)
    return {'ok': True}
