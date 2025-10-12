import uuid
from typing import Optional, Any
from pydantic import BaseModel


class QuestionBase(BaseModel):
    category: Optional[str] = None
    text: str
    type: str
    metadata_json: Optional[Any] = None


class QuestionCreate(QuestionBase):
    input_pool_id: uuid.UUID


class QuestionUpdate(BaseModel):
    category: Optional[str] = None
    text: Optional[str] = None
    type: Optional[str] = None
    metadata_json: Optional[Any] = None


class QuestionInDB(QuestionBase):
    id: uuid.UUID
    input_pool_id: uuid.UUID

    class Config:
        from_attributes = True


class QuestionResponse(QuestionBase):
    id: uuid.UUID
    input_pool_id: uuid.UUID

    class Config:
        from_attributes = True
