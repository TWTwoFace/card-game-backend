from pydantic import BaseModel, Field


class UserStatisticsSchema(BaseModel):
    user_id: int
    win_count: int = Field(ge=0)
    matches_count: int = Field(ge=0)
    max_rating: int = Field(ge=0)
    current_rating: int = Field(ge=0)