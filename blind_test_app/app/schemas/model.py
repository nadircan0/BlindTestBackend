import uuid
from typing import Optional, Any
from pydantic import BaseModel


class ModelBase(BaseModel):
    name: str
    api_key: str
    model_string: str
    config_json: Optional[Any] = None
    is_active: bool = True


class ModelCreate(ModelBase):
    pass


class ModelUpdate(BaseModel):
    name: Optional[str] = None
    api_key: Optional[str] = None
    model_string: Optional[str] = None
    config_json: Optional[Any] = None
    is_active: Optional[bool] = None


class ModelInDB(ModelBase):
    id: uuid.UUID
    admin_id: uuid.UUID

    class Config:
        from_attributes = True


class ModelResponse(ModelBase):
    id: uuid.UUID
    admin_id: uuid.UUID

    class Config:
        from_attributes = True
