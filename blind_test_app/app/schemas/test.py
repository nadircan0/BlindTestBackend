import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TestBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str  # DRAFT, ACTIVE, COMPLETED


class TestCreate(TestBase):
    input_pool_id: uuid.UUID


class TestUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class TestInDB(TestBase):
    id: uuid.UUID
    admin_id: uuid.UUID
    input_pool_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class TestResponse(TestBase):
    id: uuid.UUID
    admin_id: uuid.UUID
    input_pool_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
