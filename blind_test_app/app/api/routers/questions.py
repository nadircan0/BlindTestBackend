import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud import question
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate
from app.api.deps import get_current_admin_user
from app.db.models.user import User

router = APIRouter()


@router.post("/", response_model=QuestionResponse)
def create_question(
    question_in: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create new question"""
    return question.create(db, obj_in=question_in)


@router.get("/", response_model=List[QuestionResponse])
def get_questions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List all questions"""
    questions = question.get_multi(db, skip=skip, limit=limit)
    return questions


@router.get("/pool/{pool_id}", response_model=List[QuestionResponse])
def get_questions_by_pool(
    pool_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List questions by input pool"""
    questions = question.get_by_pool(db, pool_id=pool_id, skip=skip, limit=limit)
    return questions


@router.get("/category/{category}", response_model=List[QuestionResponse])
def get_questions_by_category(
    category: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List questions by category"""
    questions = question.get_by_category(db, category=category, skip=skip, limit=limit)
    return questions


@router.get("/type/{question_type}", response_model=List[QuestionResponse])
def get_questions_by_type(
    question_type: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List questions by type"""
    questions = question.get_by_type(db, question_type=question_type, skip=skip, limit=limit)
    return questions


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get question by ID"""
    db_question = question.get(db, question_id)
    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    return db_question


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: uuid.UUID,
    question_update: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update question"""
    # Check if question exists
    db_question = question.get(db, question_id)
    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Update question
    updated_question = question.update(db, db_obj=db_question, obj_in=question_update)
    return updated_question


@router.delete("/{question_id}")
def delete_question(
    question_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete question"""
    # Check if question exists
    db_question = question.get(db, question_id)
    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Delete question
    deleted_question = question.remove(db, question_id)
    return {"message": "Question deleted successfully", "deleted_question_id": str(question_id)}
