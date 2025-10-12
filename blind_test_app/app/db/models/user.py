import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    HEAD = "HEAD"
    JUDGE = "JUDGE"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by_admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # relations
    created_by_admin = relationship("User", remote_side=[id], backref="created_judges")
    
    # Test relations
    created_tests = relationship("Test", back_populates="admin")
    created_models = relationship("Model", back_populates="admin")
    created_input_pools = relationship("InputPool", back_populates="admin")
    answer_logs = relationship("AnswerLog", back_populates="judge")
