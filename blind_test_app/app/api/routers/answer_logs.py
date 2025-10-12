import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud import answer_log
from app.schemas.answer_log import AnswerLogCreate, AnswerLogResponse, AnswerLogUpdate
from app.api.deps import get_current_admin_user, get_current_judge_user
from app.db.models.user import User

router = APIRouter()


@router.post("/", response_model=AnswerLogResponse)
def create_answer_log(
    answer_log_in: AnswerLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_judge_user)
):
    """Create new answer log"""
    # Get judge ID from current user
    answer_log_in.judge_id = current_user.id
    return answer_log.create(db, obj_in=answer_log_in)


@router.get("/", response_model=List[AnswerLogResponse])
def get_answer_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List all answer logs"""
    logs = answer_log.get_multi(db, skip=skip, limit=limit)
    return logs


@router.get("/test/{test_id}", response_model=List[AnswerLogResponse])
def get_answer_logs_by_test(
    test_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List answer logs by test"""
    logs = answer_log.get_by_test(db, test_id=test_id, skip=skip, limit=limit)
    return logs


@router.get("/judge/{judge_id}", response_model=List[AnswerLogResponse])
def get_answer_logs_by_judge(
    judge_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List answer logs by judge"""
    logs = answer_log.get_by_judge(db, judge_id=judge_id, skip=skip, limit=limit)
    return logs


@router.get("/model/{model_id}", response_model=List[AnswerLogResponse])
def get_answer_logs_by_model(
    model_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List answer logs by model"""
    logs = answer_log.get_by_model(db, model_id=model_id, skip=skip, limit=limit)
    return logs


@router.get("/question/{question_id}", response_model=List[AnswerLogResponse])
def get_answer_logs_by_question(
    question_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List answer logs by question"""
    logs = answer_log.get_by_question(db, question_id=question_id, skip=skip, limit=limit)
    return logs


@router.get("/my", response_model=List[AnswerLogResponse])
def get_my_answer_logs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_judge_user)
):
    """List judge's own answer logs"""
    logs = answer_log.get_by_judge(db, judge_id=current_user.id, skip=skip, limit=limit)
    return logs


@router.get("/my/{log_id}", response_model=AnswerLogResponse)
def get_my_answer_log(
    log_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_judge_user)
):
    """Get judge's own answer log by ID"""
    log = answer_log.get(db, log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer log not found"
        )
    # Can only see own logs
    if log.judge_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this answer log"
        )
    return log


@router.get("/{log_id}", response_model=AnswerLogResponse)
def get_answer_log(
    log_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get answer log by ID"""
    log = answer_log.get(db, log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer log not found"
        )
    return log


@router.put("/{log_id}", response_model=AnswerLogResponse)
def update_answer_log(
    log_id: uuid.UUID,
    log_update: AnswerLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update answer log"""
    # Check if answer log exists
    db_log = answer_log.get(db, log_id)
    if not db_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer log not found"
        )
    
    # Update answer log
    updated_log = answer_log.update(db, db_obj=db_log, obj_in=log_update)
    return updated_log


@router.delete("/{log_id}")
def delete_answer_log(
    log_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete answer log"""
    # Check if answer log exists
    db_log = answer_log.get(db, log_id)
    if not db_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer log not found"
        )
    
    # Delete answer log
    deleted_log = answer_log.remove(db, log_id)
    return {"message": "Answer log deleted successfully", "deleted_log_id": str(log_id)}
