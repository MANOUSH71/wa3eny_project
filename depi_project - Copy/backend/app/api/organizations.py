from fastapi import APIRouter
from app.models.organization import OrganizationStats, DepartmentUpdate
from datetime import datetime

router = APIRouter()

@router.get("/stats", response_model=OrganizationStats)
async def get_stats():
    return OrganizationStats(
        total_attempts=120,
        total_departments=5,
        average_score=72.5,
        high_risk_departments=2,
        last_updated=datetime.now()
    )

@router.post("/departments/update")
async def update_dept(update: DepartmentUpdate):
    return {"success": True, "message": "Updated"}
