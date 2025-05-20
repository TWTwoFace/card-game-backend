from typing import Optional

from src.config.cards import CARD_BASE_POWER, UPGRADE_COST_MULTIPLIER, POWER_PER_UPGRADE
from src.database import database as db
from src.models.cards import CardSchema
from src.repositories.users import UserRepository


class CardRepository:
    @staticmethod
    async def add_card(user_id: int, card_id: int) -> bool:
        try:
            record = await db.fetchone(f"SELECT COUNT(*) FROM cards WHERE user_id='{user_id}' AND card_id='{card_id}'")
            if record["count"] != 0:
                return False

            await db.execute(f"INSERT INTO cards (user_id, card_id, power)"
                             f"VALUES ('{user_id}', '{card_id}', '{CARD_BASE_POWER[card_id]}')")

            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def upgrade_card(user_id: int, card_id: int) -> bool:
        try:
            user = await UserRepository.get_user_by_id(user_id)

            record = await db.fetchone(f"SELECT * FROM cards WHERE user_id='{user_id}' AND id='{card_id}'")
            card = CardSchema(**record)

            result = await UserRepository.change_money(user.id, user.money - card.level * UPGRADE_COST_MULTIPLIER)

            if not result:
                return False

            await db.execute(f"UPDATE cards SET level=level+1, power=power+'{POWER_PER_UPGRADE}' "
                             f"WHERE user_id='{user.id}' AND id={card_id}")

            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def get_cards_by_user_id(user_id: int) -> Optional[list[CardSchema]]:
        try:
            record = await db.fetchmany(f"SELECT * FROM cards WHERE user_id='{user_id}'")

            cards = [CardSchema(**i) for i in record]

            return cards
        except Exception as e:
            print(e)



