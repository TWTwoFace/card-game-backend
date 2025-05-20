from typing import Optional

from src.database import database as db
from src.models.shops import SellItemSchema
from src.repositories.cards import CardRepository
from src.repositories.users import UserRepository


class ShopRepository:
    @staticmethod
    async def get_last_shop() -> Optional[list[SellItemSchema]]:
        try:
            record = await db.fetchone(f"SELECT * FROM shops ORDER BY update_date LIMIT 1")
            shop_id = record['id']

            if shop_id is None:
                return None

            record = await db.fetchmany(f"SELECT * FROM sell_items WHERE sell_items.id "
                                        f"IN (SELECT sell_item_id FROM shops_sell_items WHERE shop_id='{shop_id}')")
            sell_items = [SellItemSchema(**i) for i in record]

            if record is None or len(sell_items) == 0:
                return

            return sell_items
        except Exception as e:
            print(e)

    @staticmethod
    async def buy_card(user_id: int, sell_item_id: int) -> bool:
        try:
            user = await UserRepository.get_user_by_id(user_id)

            record = await db.fetchone(f"SELECT * FROM sell_items WHERE id='{sell_item_id}'")
            sell_item = SellItemSchema(**record)

            if record is None or sell_item is None:
                return False

            if user.money < user.money - sell_item.cost:
                return False

            result = await CardRepository.add_card(user_id, sell_item.card_id)

            if not result:
                return False

            result = await UserRepository.change_money(user.id, user.money - sell_item.cost)
            return result
        except Exception as e:
            print(e)
            return False

