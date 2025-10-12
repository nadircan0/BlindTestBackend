import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud import test
from app.schemas.test import TestCreate, TestResponse, TestUpdate
from app.api.deps import get_current_admin_user, get_current_head_user, get_current_judge_user
from app.db.models.user import User

router = APIRouter()


@router.post("/", response_model=TestResponse)
def create_test(
    test_in: TestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create new test"""
    return test.create(db, obj_in=test_in, admin_id=current_user.id)


@router.get("/", response_model=List[TestResponse])
def get_tests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List all tests"""
    tests = test.get_multi(db, skip=skip, limit=limit)
    return tests


@router.get("/active", response_model=List[TestResponse])
def get_active_tests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_head_user)
):
    """List active tests"""
    tests = test.get_by_status(db, status="ACTIVE", skip=skip, limit=limit)
    return tests


@router.get("/active/judge", response_model=List[TestResponse])
def get_active_tests_for_judge(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_judge_user)
):
    """List active tests for judge"""
    tests = test.get_by_status(db, status="ACTIVE", skip=skip, limit=limit)
    return tests


@router.get("/{test_id}/judge")
def get_test_details_for_judge(
    test_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_judge_user)
):
    """Get test details for judge - Only active tests"""
    test_obj = test.get(db, test_id=test_id)
    if not test_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    # Can only see active tests
    if test_obj.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This test is not active"
        )
    return test_obj


@router.get("/{test_id}", response_model=TestResponse)
def get_test(
    test_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get test by ID"""
    db_test = test.get(db, test_id)
    if not db_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    return db_test


@router.put("/{test_id}", response_model=TestResponse)
def update_test(
    test_id: uuid.UUID,
    test_update: TestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update test"""
    # Check if test exists
    db_test = test.get(db, test_id)
    if not db_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    # Update test
    updated_test = test.update(db, db_obj=db_test, obj_in=test_update)
    return updated_test


@router.delete("/{test_id}")
def delete_test(
    test_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete test"""
    # Check if test exists
    db_test = test.get(db, test_id)
    if not db_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    # Delete test
    deleted_test = test.remove(db, test_id)
    return {"message": "Test deleted successfully", "deleted_test_id": str(test_id)}