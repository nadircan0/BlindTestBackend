import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base


class Model(Base):
    __tablename__ = "models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    api_key = Column(String, nullable=False)
    model_string = Column(String, nullable=False)
    config_json = Column(JSONB, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # relations
    admin = relationship("User", back_populates="created_models")
    answer_logs = relationship("AnswerLog", back_populates="model")
