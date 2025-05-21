from typing import Optional

from pydantic import BaseModel


class MatchmakingRoom(BaseModel):
    id: int
    host_id: int
    peer_id: Optional[int]
    state: bool


class MatchStatistics(BaseModel):
    id: int
    host_id: int
    peer_id: int
    result: bool
    duration: int
