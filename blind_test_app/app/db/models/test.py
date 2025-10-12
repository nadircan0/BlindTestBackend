import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base


class InputPool(Base):
    __tablename__ = "input_pools"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relations
    admin = relationship("User", back_populates="created_input_pools")
    questions = relationship("Question", back_populates="input_pool")
    tests = relationship("Test", back_populates="input_pool")


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    input_pool_id = Column(UUID(as_uuid=True), ForeignKey("input_pools.id"), nullable=False)
    category = Column(String, nullable=True)
    text = Column(String, nullable=False)
    type = Column(String, nullable=False)
    metadata_json = Column(JSONB, nullable=True)

    # relations
    input_pool = relationship("InputPool", back_populates="questions")
    answer_logs = relationship("AnswerLog", back_populates="question")


class Test(Base):
    __tablename__ = "tests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    input_pool_id = Column(UUID(as_uuid=True), ForeignKey("input_pools.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)  # DRAFT, ACTIVE, COMPLETED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relations
    admin = relationship("User", back_populates="created_tests")
    input_pool = relationship("InputPool", back_populates="tests")
    answer_logs = relationship("AnswerLog", back_populates="test")


class AnswerLog(Base):
    __tablename__ = "answer_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_id = Column(UUID(as_uuid=True), ForeignKey("tests.id"), nullable=False)
    judge_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    model_id = Column(UUID(as_uuid=True), ForeignKey("models.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    model_response = Column(String, nullable=False)
    duration_seconds = Column(JSONB, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relations
    test = relationship("Test", back_populates="answer_logs")
    judge = relationship("User", back_populates="answer_logs")
    model = relationship("Model", back_populates="answer_logs")
    question = relationship("Question", back_populates="answer_logs")
