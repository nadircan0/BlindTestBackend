import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud import model
from app.schemas.model import ModelCreate, ModelResponse, ModelUpdate
from app.api.deps import get_current_admin_user
from app.db.models.user import User

router = APIRouter()


@router.post("/", response_model=ModelResponse)
def create_model(
    model_in: ModelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create new model"""
    return model.create(db, obj_in=model_in, admin_id=current_user.id)


@router.get("/", response_model=List[ModelResponse])
def get_models(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List all models"""
    models = model.get_multi(db, skip=skip, limit=limit)
    return models


@router.get("/active", response_model=List[ModelResponse])
def get_active_models(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """List active models"""
    models = model.get_active_models(db, skip=skip, limit=limit)
    return models


@router.get("/{model_id}", response_model=ModelResponse)
def get_model(
    model_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get model by ID"""
    db_model = model.get(db, model_id)
    if not db_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    return db_model


@router.put("/{model_id}", response_model=ModelResponse)
def update_model(
    model_id: uuid.UUID,
    model_update: ModelUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update model"""
    # Check if model exists
    db_model = model.get(db, model_id)
    if not db_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    # Update model
    updated_model = model.update(db, db_obj=db_model, obj_in=model_update)
    return updated_model


@router.delete("/{model_id}")
def delete_model(
    model_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete model"""
    # Check if model exists
    db_model = model.get(db, model_id)
    if not db_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    # Delete model
    deleted_model = model.remove(db, model_id)
    return {"message": "Model deleted successfully", "deleted_model_id": str(model_id)}
