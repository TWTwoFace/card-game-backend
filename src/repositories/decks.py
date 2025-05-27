from typing import Optional

from src.config.decks import DECK_CAPACITY
from src.database import database as db
from src.models.cards import CardSchema
from src.models.decks import DeckSchema


class DeckRepository:
    @staticmethod
    async def create_deck(user_id: int, deck_number: int) -> bool:
        try:
            record = await db.fetchone(f"SELECT COUNT(*) "
                                       f"FROM decks WHERE deck_number='{deck_number}' and user_id='{user_id}'")

            if record['count'] > 0:
                return False

            await db.execute(f"INSERT INTO decks (user_id, deck_number) "
                             f"VALUES ('{user_id}', '{deck_number}')")

            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def add_card_to_deck(user_id: int, card_id: int, deck_number: int) -> bool:
        try:
            record = await db.fetchone(f"SELECT * FROM decks WHERE user_id='{user_id}' AND deck_number='{deck_number}'")
            deck = DeckSchema(**record)

            record = await db.fetchone(f"SELECT COUNT(*) FROM cards WHERE user_id='{user_id}' AND deck_id='{deck.id}'")

            if record['count'] >= DECK_CAPACITY:
                return False

            await db.execute(f"UPDATE cards SET deck_id='{deck.id}' WHERE id='{card_id}' AND user_id='{user_id}'")
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def remove_card_from_deck(user_id: int, card_id: int) -> bool:
        try:
            await db.execute(f"UPDATE cards SET deck_id=NULL WHERE id='{card_id}' AND user_id='{user_id}'")
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def get_user_deck(user_id: int, deck_number: int) -> Optional[list[CardSchema]]:
        try:
            record = await db.fetchone(f"SELECT * FROM decks WHERE deck_number='{deck_number}'")
            deck = DeckSchema(**record)

            record = await db.fetchmany(f"SELECT * FROM cards WHERE user_id='{user_id}' AND deck_id='{deck.id}'")
            cards = [CardSchema(**i) for i in record]

            return cards
        except Exception as e:
            print(e)
