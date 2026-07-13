from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    name: str
    points: int = 0
    badge: Optional[str] = None

class LeaderboardEntry(BaseModel):
    rank: int
    name: str
    points: int
    badge: Optional[str] = None
    is_current_user: bool = False
