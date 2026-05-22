from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    evaluator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Float)
    comment = Column(Text)
    decision = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("Application")
    evaluator = relationship("User")