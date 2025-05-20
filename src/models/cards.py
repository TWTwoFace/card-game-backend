from typing import Optional

from pydantic import BaseModel, Field


class CardCreationSchema(BaseModel):
    card_id: int = Field(ge=0, le=9)


class CardSchema(CardCreationSchema):
    id: int
    deck_id: Optional[int]
    user_id: int
    level: int = Field(ge=1, le=10)
    power: float
