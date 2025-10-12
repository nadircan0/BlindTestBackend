import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models.model import Model
from app.schemas.model import ModelCreate, ModelUpdate
from app.db.crud import user
from app.core.exceptions import raise_foreign_key_violation


class CRUDModel:
    def get(self, db: Session, model_id: uuid.UUID) -> Optional[Model]:
        return db.query(Model).filter(Model.id == model_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Model]:
        return db.query(Model).offset(skip).limit(limit).all()

    def get_by_admin(self, db: Session, admin_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Model]:
        return db.query(Model).filter(Model.admin_id == admin_id).offset(skip).limit(limit).all()

    def get_active_models(self, db: Session, skip: int = 0, limit: int = 100) -> List[Model]:
        return db.query(Model).filter(Model.is_active == True).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: ModelCreate, admin_id: uuid.UUID) -> Model:
        # Foreign key validations
        if not user.get(db, admin_id):
            raise_foreign_key_violation("admin")
        
        db_obj = Model(
            admin_id=admin_id,
            name=obj_in.name,
            api_key=obj_in.api_key,
            model_string=obj_in.model_string,
            config_json=obj_in.config_json,
            is_active=obj_in.is_active
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Model, obj_in: ModelUpdate) -> Model:
        if obj_in.name:
            db_obj.name = obj_in.name
        if obj_in.api_key:
            db_obj.api_key = obj_in.api_key
        if obj_in.model_string:
            db_obj.model_string = obj_in.model_string
        if obj_in.config_json is not None:
            db_obj.config_json = obj_in.config_json
        if obj_in.is_active is not None:
            db_obj.is_active = obj_in.is_active
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, model_id: uuid.UUID) -> Optional[Model]:
        obj = db.query(Model).get(model_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# Global instance
model = CRUDModel()
