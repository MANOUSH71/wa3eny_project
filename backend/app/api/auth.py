from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.auth import (
    UserRegister,
    UserLogin,
    TokenResponse,
    UserPublic,
    JoinOrganizationRequest
)
from app.services.auth_service import (
    create_user,
    create_employee_in_organization,
    authenticate_user,
    create_access_token,
    verify_token,
    get_user_by_id
)
from app.core.config import settings

router = APIRouter()

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserPublic:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user_id = verify_token(token)
    if user_id is None:
        raise credentials_exception
    
    user = get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    
    return UserPublic(
    id=user.id,
    name=user.name,
    email=user.email,
    role=user.role,
    organization_name=user.organization_name,
    organization_id=user.organization_id,
    organization_code=user.organization_code,
    department=user.department,
    created_at=user.created_at
)

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister):
    """Register a new user"""
    try:
        # Create user
        user = create_user(user_data)
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            user=user
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )
    

@router.post("/join-organization", response_model=TokenResponse)
async def join_organization(
    employee_data: JoinOrganizationRequest
):
    """Register an employee using an organization code."""

    try:
        employee = create_employee_in_organization(employee_data)

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        access_token = create_access_token(
            data={"sub": employee.id},
            expires_delta=access_token_expires
        )

        return TokenResponse(
            access_token=access_token,
            user=employee
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to join organization: {str(error)}"
        )

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user with email and password"""
    # Authenticate user
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    user_public = UserPublic(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        organization_name=user.organization_name,
        organization_id=user.organization_id,
        created_at=user.created_at
    )
    
    return TokenResponse(
        access_token=access_token,
        user=user_public
    )

@router.post("/login-json", response_model=TokenResponse)
async def login_json(login_data: UserLogin):
    """Login user with JSON payload (alternative to form data)"""
    # Authenticate user
    user = authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    user_public = UserPublic(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        organization_name=user.organization_name,
        organization_id=user.organization_id,
        created_at=user.created_at
    )
    
    return TokenResponse(
        access_token=access_token,
        user=user_public
    )

@router.get("/me", response_model=UserPublic)
async def get_me(current_user: UserPublic = Depends(get_current_user)):
    """Get current user information"""
    return current_user