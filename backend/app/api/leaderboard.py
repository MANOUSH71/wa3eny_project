from fastapi import APIRouter
from app.models.user import LeaderboardEntry

router = APIRouter()

@router.get("/", response_model=list[LeaderboardEntry])
async def get_leaderboard():
    return [
        LeaderboardEntry(rank=1, name="Mona Abdallah", points=260, badge="Silver 🥈"),
        LeaderboardEntry(rank=2, name="Youssef El-Sherif", points=140, badge="Bronze 🥉"),
        LeaderboardEntry(rank=3, name="Sara Kamal", points=60, badge="Bronze 🥉")
    ]
