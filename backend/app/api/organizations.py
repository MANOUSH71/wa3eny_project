from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.organization import (
    OrganizationStats,
    DepartmentUpdate,
    OrganizationPublic
)

from app.models.auth import UserPublic

from app.api.auth import get_current_user

from app.services.organization_service import (
    get_organization_by_owner
)


router = APIRouter()


@router.get("/me", response_model=OrganizationPublic)
async def get_my_organization(
    current_user: UserPublic = Depends(get_current_user)
):
    """
    Return the organization owned by the logged-in organization admin.
    """

    if current_user.role not in [
        "organization_admin",
        "organization"
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organization admins can access this resource."
        )

    organization = get_organization_by_owner(
        current_user.id
    )

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found."
        )

    return OrganizationPublic(
        id=organization.id,
        organization_name=organization.organization_name,
        organization_code=organization.organization_code,
        owner_user_id=organization.owner_user_id,
        created_at=organization.created_at
    )


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
    return {
        "success": True,
        "message": "Updated"
    }