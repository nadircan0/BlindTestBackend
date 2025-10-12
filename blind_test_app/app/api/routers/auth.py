from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, verify_refresh_token
from app.db.session import get_db
from app.db.crud import user
from app.schemas.user import Token, UserSignup, UserResponse, RefreshTokenRequest
from pydantic import BaseModel
from app.api.deps import get_current_user
from app.db.models.user import User
from app.core.exceptions import raise_email_already_exists, raise_inactive_user

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/signup", response_model=UserResponse)
def signup(
    user_data: UserSignup,
    db: Session = Depends(get_db)
):
    """User registration"""
    # Check if email is already registered
    existing_user = user.get_by_email(db, email=user_data.email)
    if existing_user:
        raise_email_already_exists()
    
    # Create new user (default role is JUDGE)
    from app.db.models.user import UserRole
    from app.schemas.user import UserCreate
    
    user_create_data = UserCreate(
        email=user_data.email,
        password=user_data.password,
        role=UserRole.JUDGE,  # Default role
        name=user_data.name,
        surname=user_data.surname,
        phone=user_data.phone,
        is_active=True
    )
    
    new_user = user.create(db, obj_in=user_create_data)
    return new_user


@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """User login and token creation"""
    current_user = user.authenticate(db, email=login_data.email, password=login_data.password)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active(current_user):
        raise_inactive_user()
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        subject=current_user.email, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        subject=current_user.email, expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



@router.post("/refresh", response_model=Token)
def refresh_access_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    email = verify_refresh_token(refresh_data.refresh_token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    current_user = user.get_by_email(db, email=email)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active(current_user):
        raise_inactive_user()
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        subject=current_user.email, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        subject=current_user.email, expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user
