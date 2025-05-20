from typing import Optional, Union, Annotated

from pydantic import BaseModel, Field


class ClanCreatingSchema(BaseModel):
    name: str = Field(min_length=5, max_length=20)
    description: str = Field(min_length=5, max_length=100)
    avatar: int = Field(ge=0, le=9)


class ClanSchema(ClanCreatingSchema):
    id: int
    owner_id: int


class ClanChangeSchema(BaseModel):
    description: Annotated[Optional[str], Field(min_length=5, max_length=100)] = None
    avatar: Annotated[Optional[int], Field(ge=0, le=9)] = None


class ClanActionCreationSchema(BaseModel):
    description: str = Field(min_length=5, max_length=100)


class ClanActionSchema(ClanActionCreationSchema):
    id: int
    user_id: int
    clan_id: int
