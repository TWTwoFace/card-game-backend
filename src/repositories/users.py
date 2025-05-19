from fastapi import HTTPException

from src.database import database as db
from src.models.users import UserRegisterSchema, UserSchema, UserLoginSchema


class UserRepository:
    @staticmethod
    async def create_user(user: UserRegisterSchema) -> None:
        try:
            await db.execute(f"INSERT INTO users (login, password_hash, nickname) "
                             f"VALUES ('{user.login}','{user.password}', '{user.nickname}')")

            created_user = UserSchema(**(await db.fetchone(f"SELECT * FROM users WHERE login='{user.login}'")))
            await db.execute(f"INSERT INTO statistics (user_id) VALUES ('{created_user.id}')")

        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="User with this params already exists")

    @staticmethod
    async def get_users() -> list[UserSchema]:
        try:
            record = await db.fetchmany(f"SELECT * FROM users")
            users = [UserSchema(**i) for i in record]
            return users
        except Exception as e:
            print(e)

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserSchema:
        try:
            record = await db.fetchone(f"SELECT * FROM users WHERE id='{user_id}'")
            user = UserSchema(**record)
            return user
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="User with this id doesn't exists")

    @staticmethod
    async def delete_user(user_id):
        try:
            await db.execute(f"DELETE FROM users WHERE id='{user_id}'")
        except Exception as e:
            print(e)

    @staticmethod
    async def login_user(user: UserLoginSchema) -> UserSchema:
        try:
            record = await db.fetchone(f"SELECT * FROM users "
                                       f"WHERE login='{user.login}' AND password_hash='{user.password}'")
            if record is not None:
                logged_user = UserSchema(**record)
                print(logged_user)
                return logged_user

        except Exception as e:
            print(e)


