from typing import Optional

from fastapi import HTTPException

from src.database import database as db
from src.models.clans import ClanSchema
from src.models.users import UserRegisterSchema, UserSchema, UserLoginSchema
from src.utils.security import hash_password, check_password


class UserRepository:
    @staticmethod
    async def create_user(user: UserRegisterSchema) -> None:
        try:
            await db.execute(f"INSERT INTO users (login, password_hash, nickname) "
                             f"VALUES ('{user.login}','{hash_password(user.password)}', '{user.nickname}')")

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
    async def login_user(user: UserLoginSchema) -> Optional[UserSchema]:
        try:
            record = await db.fetchone(f"SELECT * FROM users "
                                       f"WHERE login='{user.login}'")
            if record is None:
                return None

            if not check_password(user.password, record['password_hash']):
                return None

            logged_user = UserSchema(**record)
            return logged_user
        except Exception as e:
            print(e)

    @staticmethod
    async def change_money(user_id: int, new_money_count: int):
        if new_money_count < 0:
            return
        try:
            await db.execute(f"UPDATE users SET money='{new_money_count}' WHERE id='{user_id}'")

        except Exception as e:
            print(e)

    @staticmethod
    async def join_clan(user_id: int, clan_id: int) -> bool:
        try:
            record = await db.fetchone(f"SELECT * FROM users WHERE id='{user_id}'")
            user = UserSchema(**record)

            if user.clan_id is not None:
                return False

            record = await db.fetchmany(f"SELECT * FROM users WHERE clan_id='{clan_id}'")
            clan_members = [UserSchema(**i) for i in record]

            if len(clan_members) >= 30:
                return False

            await db.execute(f"UPDATE users SET clan_id='{clan_id}' WHERE id='{user_id}'")

            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def left_clan(user_id: int):
        try:
            record = await db.fetchone(f"SELECT * FROM users WHERE id='{user_id}'")
            user = UserSchema(**record)

            if user.clan_id is None:
                return False

            record = await db.fetchone(f"SELECT * FROM clans WHERE id='{user.clan_id}'")
            clan = ClanSchema(**record)

            if clan is not None and clan.owner_id == user.id:
                return False

            await db.execute(f"UPDATE users SET clan_id=NULL WHERE id='{user.id}'")

            return True
        except Exception as e:
            print(e)
            return False

