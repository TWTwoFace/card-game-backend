from pydantic import BaseModel, Field


class SellItemSchema(BaseModel):
    id: int
    card_id: int = Field(ge=0, le=9)
    cost: int = Field(ge=0)


class ShopSellItemSchema(BaseModel):
    shop_id: int
    sell_item_id: int
