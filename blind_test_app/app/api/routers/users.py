import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud import user
from app.schemas.user import UserCreate, UserResponse, JudgeCreate, UserUpdate
from app.api.deps import get_current_admin_user, get_current_head_user
from app.db.models.user import User, UserRole

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create new user"""
    db_user = user.get_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already registered"
        )
    return user.create(db, obj_in=user_in, created_by_admin_id=current_user.id)


@router.post("/judges", response_model=UserResponse)
def create_judge(
    judge_in: JudgeCreate,
    password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create new judge"""
    db_user = user.get_by_email(db, email=judge_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already registered"
        )
    return user.create_judge(db, obj_in=judge_in, admin_id=current_user.id, password=password)


@router.post("/judges/head", response_model=UserResponse)
def create_judge_by_head(
    judge_in: JudgeCreate,
    password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_head_user)
):
    """Create new judge by HEAD role"""
    db_user = user.get_by_email(db, email=judge_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already registered"
        )
    return user.create_judge(db, obj_in=judge_in, admin_id=current_user.id, password=password)


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List all users"""
    users = user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/judges", response_model=List[UserResponse])
def get_judges(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List all judges"""
    judges = user.get_by_role(db, role=UserRole.JUDGE, skip=skip, limit=limit)
    return judges


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get user by ID"""
    db_user = user.get(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: uuid.UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update user"""
    # Check if user exists
    db_user = user.get(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if email is already taken by another user
    if user_update.email and user_update.email != db_user.email:
        existing_user = user.get_by_email(db, email=user_update.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email address already registered"
            )
    
    # Update user
    updated_user = user.update(db, db_obj=db_user, obj_in=user_update)
    return updated_user


@router.delete("/{user_id}")
def delete_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete user"""
    # Check if user exists
    db_user = user.get(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from deleting themselves
    if db_user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Delete user
    deleted_user = user.remove(db, user_id)
    return {"message": "User deleted successfully", "deleted_user_id": str(user_id)}
