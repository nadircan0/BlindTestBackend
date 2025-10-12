import uuid
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy.orm import Session
from app.core.security import verify_token
from app.core.exceptions import raise_invalid_credentials, raise_insufficient_permissions
from app.db.session import get_db
from app.db.crud import user
from app.db.models.user import User, UserRole

# HTTP Bearer scheme (sadece token ile)
bearer_scheme = HTTPBearer()


def get_current_user(
    db: Session = Depends(get_db),
    credentials = Depends(bearer_scheme)
) -> User:
    """Get current user with bearer token"""
    token = credentials.credentials
    email = verify_token(token)
    if email is None:
        raise_invalid_credentials()
    
    current_user = user.get_by_email(db, email=email)
    if current_user is None:
        raise_invalid_credentials()
    
    return current_user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Check active user"""
    if not user.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Check admin user"""
    if not user.is_admin(current_user):
        raise_insufficient_permissions()
    return current_user


def get_current_head_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Check head user"""
    if not user.is_head(current_user):
        raise_insufficient_permissions()
    return current_user


def get_current_judge_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Check judge user"""
    if not user.is_judge(current_user):
        raise_insufficient_permissions()
    return current_user
