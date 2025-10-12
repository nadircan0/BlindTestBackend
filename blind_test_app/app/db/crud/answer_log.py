import uuid
from typing import Optional, List, Any
from sqlalchemy.orm import Session
from app.db.models.test import AnswerLog
from app.schemas.answer_log import AnswerLogCreate, AnswerLogUpdate
from app.db.crud import test, model, question, user
from app.core.exceptions import raise_foreign_key_violation


class CRUDAnswerLog:
    def get(self, db: Session, log_id: uuid.UUID) -> Optional[AnswerLog]:
        return db.query(AnswerLog).filter(AnswerLog.id == log_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[AnswerLog]:
        return db.query(AnswerLog).offset(skip).limit(limit).all()

    def get_by_test(self, db: Session, test_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[AnswerLog]:
        return db.query(AnswerLog).filter(AnswerLog.test_id == test_id).offset(skip).limit(limit).all()

    def get_by_judge(self, db: Session, judge_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[AnswerLog]:
        return db.query(AnswerLog).filter(AnswerLog.judge_id == judge_id).offset(skip).limit(limit).all()

    def get_by_model(self, db: Session, model_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[AnswerLog]:
        return db.query(AnswerLog).filter(AnswerLog.model_id == model_id).offset(skip).limit(limit).all()

    def get_by_question(self, db: Session, question_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[AnswerLog]:
        return db.query(AnswerLog).filter(AnswerLog.question_id == question_id).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: AnswerLogCreate) -> AnswerLog:
        # Foreign key validations
        if not test.get(db, obj_in.test_id):
            raise_foreign_key_violation("test")
        
        if not model.get(db, obj_in.model_id):
            raise_foreign_key_violation("model")
        
        if not question.get(db, obj_in.question_id):
            raise_foreign_key_violation("question")
        
        if obj_in.judge_id and not user.get(db, obj_in.judge_id):
            raise_foreign_key_violation("judge")
        
        db_obj = AnswerLog(
            test_id=obj_in.test_id,
            judge_id=obj_in.judge_id,
            model_id=obj_in.model_id,
            question_id=obj_in.question_id,
            model_response=obj_in.model_response,
            duration_seconds=obj_in.duration_seconds
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: AnswerLog, obj_in: AnswerLogUpdate) -> AnswerLog:
        if obj_in.model_response:
            db_obj.model_response = obj_in.model_response
        if obj_in.duration_seconds is not None:
            db_obj.duration_seconds = obj_in.duration_seconds
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, log_id: uuid.UUID) -> Optional[AnswerLog]:
        obj = db.query(AnswerLog).get(log_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# Global instance
answer_log = CRUDAnswerLog()
