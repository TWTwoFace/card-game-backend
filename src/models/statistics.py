from pydantic import BaseModel, Field


class UserStatisticsSchema(BaseModel):
    id: int
    user_id: int
    win_count: int = Field(ge=0)
    matches_count: int = Field(ge=0)
    max_rating: int = Field(ge=0)
    current_rating: int = Field(ge=0)