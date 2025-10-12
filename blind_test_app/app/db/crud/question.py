import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models.test import Question
from app.schemas.question import QuestionCreate, QuestionUpdate
from app.db.crud import input_pool
from app.core.exceptions import raise_foreign_key_violation


class CRUDQuestion:
    def get(self, db: Session, question_id: uuid.UUID) -> Optional[Question]:
        return db.query(Question).filter(Question.id == question_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Question]:
        return db.query(Question).offset(skip).limit(limit).all()

    def get_by_pool(self, db: Session, pool_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Question]:
        return db.query(Question).filter(Question.input_pool_id == pool_id).offset(skip).limit(limit).all()

    def get_by_category(self, db: Session, category: str, skip: int = 0, limit: int = 100) -> List[Question]:
        return db.query(Question).filter(Question.category == category).offset(skip).limit(limit).all()

    def get_by_type(self, db: Session, question_type: str, skip: int = 0, limit: int = 100) -> List[Question]:
        return db.query(Question).filter(Question.type == question_type).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: QuestionCreate) -> Question:
        # Foreign key validations
        if not input_pool.get(db, obj_in.input_pool_id):
            raise_foreign_key_violation("input pool")
        
        db_obj = Question(
            input_pool_id=obj_in.input_pool_id,
            category=obj_in.category,
            text=obj_in.text,
            type=obj_in.type,
            metadata_json=obj_in.metadata_json
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Question, obj_in: QuestionUpdate) -> Question:
        if obj_in.category is not None:
            db_obj.category = obj_in.category
        if obj_in.text:
            db_obj.text = obj_in.text
        if obj_in.type:
            db_obj.type = obj_in.type
        if obj_in.metadata_json is not None:
            db_obj.metadata_json = obj_in.metadata_json
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, question_id: uuid.UUID) -> Optional[Question]:
        obj = db.query(Question).get(question_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# Global instance
question = CRUDQuestion()
