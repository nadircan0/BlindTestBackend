import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel


class AnswerLogBase(BaseModel):
    model_response: str
    duration_seconds: Any


class AnswerLogCreate(AnswerLogBase):
    test_id: uuid.UUID
    model_id: uuid.UUID
    question_id: uuid.UUID
    judge_id: uuid.UUID = None  # Will be set automatically by server


class AnswerLogUpdate(BaseModel):
    model_response: str
    duration_seconds: Any


class AnswerLogInDB(AnswerLogBase):
    id: uuid.UUID
    test_id: uuid.UUID
    judge_id: uuid.UUID
    model_id: uuid.UUID
    question_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class AnswerLogResponse(AnswerLogBase):
    id: uuid.UUID
    test_id: uuid.UUID
    judge_id: uuid.UUID
    model_id: uuid.UUID
    question_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
