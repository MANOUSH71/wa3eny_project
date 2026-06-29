from pydantic import BaseModel
from datetime import datetime

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
