import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud import input_pool
from app.schemas.input_pool import InputPoolCreate, InputPoolResponse, InputPoolUpdate
from app.api.deps import get_current_admin_user
from app.db.models.user import User

router = APIRouter()


@router.post("/", response_model=InputPoolResponse)
def create_input_pool(
    pool_in: InputPoolCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create new input pool"""
    return input_pool.create(db, obj_in=pool_in, admin_id=current_user.id)


@router.get("/", response_model=List[InputPoolResponse])
def get_input_pools(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List all input pools"""
    pools = input_pool.get_multi(db, skip=skip, limit=limit)
    return pools


@router.get("/{pool_id}", response_model=InputPoolResponse)
def get_input_pool(
    pool_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get input pool by ID"""
    db_pool = input_pool.get(db, pool_id)
    if not db_pool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Input pool not found"
        )
    return db_pool


@router.put("/{pool_id}", response_model=InputPoolResponse)
def update_input_pool(
    pool_id: uuid.UUID,
    pool_update: InputPoolUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update input pool"""
    # Check if input pool exists
    db_pool = input_pool.get(db, pool_id)
    if not db_pool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Input pool not found"
        )
    
    # Update input pool
    updated_pool = input_pool.update(db, db_obj=db_pool, obj_in=pool_update)
    return updated_pool


@router.delete("/{pool_id}")
def delete_input_pool(
    pool_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete input pool"""
    # Check if input pool exists
    db_pool = input_pool.get(db, pool_id)
    if not db_pool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Input pool not found"
        )
    
    # Delete input pool
    deleted_pool = input_pool.remove(db, pool_id)
    return {"message": "Input pool deleted successfully", "deleted_pool_id": str(pool_id)}
