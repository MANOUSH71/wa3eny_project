from fastapi import APIRouter
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(user: User):
    return user

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    return User(id=user_id, name="Test User", points=100)
