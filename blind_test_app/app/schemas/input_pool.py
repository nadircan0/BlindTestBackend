import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InputPoolBase(BaseModel):
    name: str
    description: Optional[str] = None


class InputPoolCreate(InputPoolBase):
    pass


class InputPoolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class InputPoolInDB(InputPoolBase):
    id: uuid.UUID
    admin_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class InputPoolResponse(InputPoolBase):
    id: uuid.UUID
    admin_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
