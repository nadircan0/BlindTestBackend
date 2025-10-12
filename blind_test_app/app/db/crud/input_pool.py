import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models.test import InputPool
from app.schemas.input_pool import InputPoolCreate, InputPoolUpdate


class CRUDInputPool:
    def get(self, db: Session, pool_id: uuid.UUID) -> Optional[InputPool]:
        return db.query(InputPool).filter(InputPool.id == pool_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[InputPool]:
        return db.query(InputPool).offset(skip).limit(limit).all()

    def get_by_admin(self, db: Session, admin_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[InputPool]:
        return db.query(InputPool).filter(InputPool.admin_id == admin_id).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: InputPoolCreate, admin_id: uuid.UUID) -> InputPool:
        db_obj = InputPool(
            admin_id=admin_id,
            name=obj_in.name,
            description=obj_in.description
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: InputPool, obj_in: InputPoolUpdate) -> InputPool:
        if obj_in.name:
            db_obj.name = obj_in.name
        if obj_in.description is not None:
            db_obj.description = obj_in.description
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, pool_id: uuid.UUID) -> Optional[InputPool]:
        obj = db.query(InputPool).get(pool_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# Global instance
input_pool = CRUDInputPool()
