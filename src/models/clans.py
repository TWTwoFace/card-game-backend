from typing import Optional, Union, Annotated

from pydantic import BaseModel, Field


class ClanCreatingScheme(BaseModel):
    name: str = Field(min_length=5, max_length=20)
    description: str = Field(min_length=5, max_length=100)
    avatar: int = Field(ge=0, le=9)


class ClanScheme(ClanCreatingScheme):
    id: int
    owner_id: int


class ClanChangeScheme(BaseModel):
    description: Annotated[Optional[str], Field(min_length=5, max_length=100)] = None
    avatar: Annotated[Optional[int], Field(ge=0, le=9)] = None
