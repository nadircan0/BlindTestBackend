import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models.test import Test
from app.schemas.test import TestCreate, TestUpdate
from app.db.crud import input_pool, user
from app.core.exceptions import raise_foreign_key_violation


class CRUDTest:
    def get(self, db: Session, test_id: uuid.UUID) -> Optional[Test]:
        return db.query(Test).filter(Test.id == test_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Test]:
        return db.query(Test).offset(skip).limit(limit).all()

    def get_by_admin(self, db: Session, admin_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Test]:
        return db.query(Test).filter(Test.admin_id == admin_id).offset(skip).limit(limit).all()

    def get_by_status(self, db: Session, status: str, skip: int = 0, limit: int = 100) -> List[Test]:
        return db.query(Test).filter(Test.status == status).offset(skip).limit(limit).all()

    def get_by_pool(self, db: Session, pool_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Test]:
        return db.query(Test).filter(Test.input_pool_id == pool_id).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: TestCreate, admin_id: uuid.UUID) -> Test:
        # Foreign key validations
        if not user.get(db, admin_id):
            raise_foreign_key_violation("admin")
        
        if not input_pool.get(db, obj_in.input_pool_id):
            raise_foreign_key_violation("input pool")
        
        db_obj = Test(
            admin_id=admin_id,
            input_pool_id=obj_in.input_pool_id,
            name=obj_in.name,
            description=obj_in.description,
            status=obj_in.status
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Test, obj_in: TestUpdate) -> Test:
        if obj_in.name:
            db_obj.name = obj_in.name
        if obj_in.description is not None:
            db_obj.description = obj_in.description
        if obj_in.status:
            db_obj.status = obj_in.status
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, test_id: uuid.UUID) -> Optional[Test]:
        obj = db.query(Test).get(test_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# Global instance
test = CRUDTest()
