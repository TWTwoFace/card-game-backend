from src.models.clans import ClanCreatingScheme, ClanScheme, ClanChangeScheme
from src.database import database as db
from src.models.users import UserSchema


class ClanRepository:
    @staticmethod
    async def create_clan(owner_id: int, clan: ClanCreatingScheme) -> bool:
        try:
            record = await db.fetchone(f"SELECT * FROM users WHERE id='{owner_id}'")
            user = UserSchema(**record)

            if record is None or user.clan_id is not None:
                return False

            await db.execute(f"INSERT INTO clans (name, description, avatar, owner_id)"
                             f"VALUES ('{clan.name}', '{clan.description}', '{clan.avatar}', '{owner_id}')")

            record = await db.fetchone(f"SELECT * FROM clans WHERE owner_id='{owner_id}'")

            clan = ClanScheme(**record)
            await db.execute(f"UPDATE users SET clan_id='{clan.id}'")

            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def change_description(owner_id: int, clan_change: ClanChangeScheme) -> bool:
        if clan_change.description is None:
            return False
        try:
            record = await db.fetchone(f"SELECT * FROM clans WHERE owner_id='{owner_id}'")
            if record is None:
                return False

            clan = ClanScheme(**record)

            await db.execute(f"UPDATE clans SET description='{clan_change.description}' WHERE id='{clan.id}'")
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def change_avatar(owner_id: int, clan_change: ClanChangeScheme) -> bool:
        if clan_change.avatar is None:
            return False
        try:
            record = await db.fetchone(f"SELECT * FROM clans WHERE owner_id='{owner_id}'")
            if record is None:
                return False

            clan = ClanScheme(**record)

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

            clan = ClanScheme(**record)

            await db.execute(f"DELETE FROM clans WHERE id='{clan.id}'")
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def get_clans() -> list[ClanScheme]:
        try:
            record = await db.fetchmany('SELECT * FROM clans')
            clans = [ClanScheme(**i) for i in record]

            return clans
        except Exception as e:
            print(e)

    @staticmethod
    async def get_clan_by_id(clan_id: int) -> ClanScheme:
        try:
            record = await db.fetchone(f"SELECT * FROM clans WHERE id='{clan_id}'")
            clan = ClanScheme(**record)

            return clan
        except Exception as e:
            print(e)
