from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # "organization_admin", "employee", "individual"
    organization_name: Optional[str] = None

class JoinOrganizationRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    organization_code: str
    department: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: str
    name: str
    email: str
    role: str
    organization_name: Optional[str] = None
    organization_id: Optional[str] = None
    organization_code: Optional[str] = None
    department: Optional[str] = None
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic

class UserInDB(BaseModel):
    id: str
    name: str
    email: str
    password_hash: str
    role: str
    organization_name: Optional[str] = None
    organization_id: Optional[str] = None
    organization_code: Optional[str] = None
    department: Optional[str] = None
    created_at: datetime