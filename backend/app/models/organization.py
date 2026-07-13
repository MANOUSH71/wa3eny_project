from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrganizationCreate(BaseModel):
    organization_name: str

class OrganizationInDB(BaseModel):
    id: str
    organization_name: str
    organization_code: str
    owner_user_id: str
    created_at: datetime

class OrganizationPublic(BaseModel):
    id: str
    organization_name: str
    organization_code: str
    owner_user_id: str
    created_at: datetime

class OrganizationResponse(BaseModel):
    id: str
    organization_name: str
    organization_code: str
    created_at: datetime

class OrganizationStats(BaseModel):
    total_attempts: int
    total_departments: int
    average_score: float
    high_risk_departments: int
    last_updated: datetime

class DepartmentUpdate(BaseModel):
    department_key: str
    score: int
    correct: bool