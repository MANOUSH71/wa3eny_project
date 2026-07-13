import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from uuid import uuid4
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.core.config import settings
from app.models.auth import (
    UserInDB,
    UserRegister,
    UserPublic,
    JoinOrganizationRequest
)
from app.models.organization import OrganizationCreate
from app.services.organization_service import (
    create_organization,
    get_organization_by_code
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# File path for local JSON storage
USERS_FILE_PATH = "backend/app/data/users.json"

def ensure_data_directory():
    """Ensure the data directory and users.json file exist"""
    os.makedirs(os.path.dirname(USERS_FILE_PATH), exist_ok=True)
    if not os.path.exists(USERS_FILE_PATH):
        with open(USERS_FILE_PATH, "w") as f:
            json.dump([], f)

def load_users() -> List[Dict[str, Any]]:
    """Load users from JSON file"""
    ensure_data_directory()
    try:
        with open(USERS_FILE_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users: List[Dict[str, Any]]):
    """Save users to JSON file"""
    ensure_data_directory()
    with open(USERS_FILE_PATH, 'w') as f:
        json.dump(users, f, indent=2, default=str)

def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Get user by email from JSON storage"""
    users = load_users()
    for user_data in users:
        if user_data["email"] == email:
            return UserInDB(**user_data)
    return None

def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    """Get user by ID from JSON storage"""
    users = load_users()
    for user_data in users:
        if user_data["id"] == user_id:
            return UserInDB(**user_data)
    return None

def create_user(user_data: UserRegister) -> UserPublic:
    """Create a new user and organization if needed."""

    # Check if user already exists
    if get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Validate role
    valid_roles = [
        "organization_admin",
        "employee",
        "individual",
        "organization"
    ]

    if user_data.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be 'organization_admin', 'employee', or 'individual'"
        )

    # Backward compatibility
    if user_data.role == "organization":
        user_data.role = "organization_admin"

    # Hash password
    password_hash = pwd_context.hash(user_data.password)

    # Generate user ID
    user_id = str(uuid4())
    organization_id = None
    organization_code = None

    # Create organization for organization admins
    if (
        user_data.role == "organization_admin"
        and user_data.organization_name
    ):
        organization_data = OrganizationCreate(
            organization_name=user_data.organization_name
        )

        organization = create_organization(
            organization_data,
            user_id
        )

        organization_id = organization.id
        organization_code = organization.organization_code

    # Create user object
    new_user = UserInDB(
        id=user_id,
        name=user_data.name,
        email=user_data.email,
        password_hash=password_hash,
        role=user_data.role,
        organization_name=user_data.organization_name,
        organization_id=organization_id,
        created_at=datetime.utcnow()
    )

    # Save user
    users = load_users()
    users.append(new_user.model_dump())
    save_users(users)

    # Return public user data
    return UserPublic(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        role=new_user.role,
        organization_name=new_user.organization_name,
        organization_id=new_user.organization_id,
        organization_code=organization_code,
        created_at=new_user.created_at
    )


def create_employee_in_organization(
    employee_data: JoinOrganizationRequest
) -> UserPublic:
    """Create an employee and connect them to an organization."""

    if get_user_by_email(employee_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    organization_code = (
        employee_data.organization_code
        .strip()
        .upper()
    )

    organization = get_organization_by_code(
        organization_code
    )

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid organization code"
        )

    department = employee_data.department.strip()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please select a department"
        )

    password_hash = pwd_context.hash(
        employee_data.password
    )

    new_employee = UserInDB(
        id=str(uuid4()),
        name=employee_data.name.strip(),
        email=employee_data.email.lower(),
        password_hash=password_hash,
        role="employee",
        organization_name=organization.organization_name,
        organization_id=organization.id,
        organization_code=organization.organization_code,
        department=department,
        created_at=datetime.utcnow()
    )

    users = load_users()
    users.append(new_employee.model_dump())
    save_users(users)

    return UserPublic(
        id=new_employee.id,
        name=new_employee.name,
        email=new_employee.email,
        role=new_employee.role,
        organization_name=new_employee.organization_name,
        organization_id=new_employee.organization_id,
        organization_code=new_employee.organization_code,
        department=new_employee.department,
        created_at=new_employee.created_at
    )

def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    """Authenticate user with email and password"""
    user = get_user_by_email(email)
    if not user:
        return None
    if not pwd_context.verify(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verify JWT token and return user ID"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None