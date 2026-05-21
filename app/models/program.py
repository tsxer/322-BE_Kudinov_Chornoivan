import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ProgramType(str, enum.Enum):
    A = "A"
    B = "B"

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ProgramType), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    rules = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    calls = relationship("Call", back_populates="program")


class CallStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    closed = "closed"

class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum(CallStatus), default=CallStatus.draft)
    deadline = Column(DateTime(timezone=True))
    criteria = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    program = relationship("Program", back_populates="calls")