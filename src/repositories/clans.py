from typing import Optional

from src.models.clans import ClanCreatingSchema, ClanSchema, ClanChangeSchema, ClanActionCreationSchema, \
    ClanActionSchema
from src.database import database as db
from src.models.users import UserSchema


class ClanRepository:
    @staticmethod
    async def create_clan(owner_id: int, clan: ClanCreatingSchema) -> bool:
        try:
            record = await db.fetchone(f"SELECT * FROM users WHERE id='{owner_id}'")
            user = UserSchema(**record)

            if record is None or user.clan_id is not None:
                return False

            await db.execute(f"INSERT INTO clans (name, description, avatar, owner_id)"
                             f"VALUES ('{clan.name}', '{clan.description}', '{clan.avatar}', '{owner_id}')")

            record = await db.fetchone(f"SELECT * FROM clans WHERE owner_id='{owner_id}'")

            clan = ClanSchema(**record)
            await db.execute(f"UPDATE users SET clan_id='{clan.id}'")

            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def change_description(owner_id: int, clan_change: ClanChangeSchema) -> bool:
        if clan_change.description is None:
            return False
        try:
            record = await db.fetchone(f"SELECT * FROM clans WHERE owner_id='{owner_id}'")
            if record is None:
                return False

            clan = ClanSchema(**record)

            await db.execute(f"UPDATE clans SET description='{clan_change.description}' WHERE id='{clan.id}'")
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def change_avatar(owner_id: int, clan_change: ClanChangeSchema) -> bool:
        if clan_change.avatar is None:
            return False
        try:
            record = await db.fetchone(f"SELECT * FROM clans WHERE owner_id='{owner_id}'")
            if record is None:
                return False

            clan = ClanSchema(**record)

            await db.execute(f"UPDATE clans SET avatar='{clan_change.avatar}' WHERE id='{clan.id}'")
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def delete_clan(owner_id: int) -> bool:
        try:
            record = await db.fetchone(f"SELECT * FROM clans WHERE owner_id='{owner_id}'")
            if record is None:
                return False

            clan = ClanSchema(**record)

            await db.execute(f"DELETE FROM clans WHERE id='{clan.id}'")
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def get_clans() -> list[ClanSchema]:
        try:
            record = await db.fetchmany('SELECT * FROM clans')
            clans = [ClanSchema(**i) for i in record]

            return clans
        except Exception as e:
            print(e)

    @staticmethod
    async def get_clan_by_id(clan_id: int) -> ClanSchema:
        try:
            record = await db.fetchone(f"SELECT * FROM clans WHERE id='{clan_id}'")
            clan = ClanSchema(**record)

            return clan
        except Exception as e:
            print(e)

    @staticmethod
    async def get_clan_members(clan_id: int) -> Optional[list[UserSchema]]:
        try:
            record = await db.fetchmany(f"SELECT * FROM users WHERE clan_id='{clan_id}'")
            users = [UserSchema(**i) for i in record]
            return users
        except Exception as e:
            print(e)

    @staticmethod
    async def create_clan_action(user_id: int, action: ClanActionCreationSchema) -> bool:
        try:
            record = await db.fetchone(f"SELECT * FROM users WHERE id='{user_id}'")
            user = UserSchema(**record)

            if record is None or user.clan_id is None:
                return False

            await db.execute(f"INSERT INTO clan_actions (user_id, clan_id, description)"
                             f"VALUES ('{user.id}', '{user.clan_id}', '{action.description}')")
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def get_clan_actions(clan_id: int) -> Optional[ClanActionSchema]:
        try:
            record = await db.fetchmany(f"SELECT * FROM clan_actions WHERE clan_id='{clan_id}'")
            actions = [ClanActionSchema(**i) for i in record]
            return actions
        except Exception as e:
            print(e)
