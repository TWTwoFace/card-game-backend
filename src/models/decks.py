from pydantic import BaseModel


class DeckSchema(BaseModel):
    id: int
    user_id: int
    deck_number: int
