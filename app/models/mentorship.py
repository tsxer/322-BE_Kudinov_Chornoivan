from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Mentorship(Base):
    __tablename__ = "mentorships"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    mentor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())

    application = relationship("Application")
    mentor = relationship("User")
    milestones = relationship("Milestone", back_populates="mentorship")
    sessions = relationship("MentorSession", back_populates="mentorship")

class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    mentorship_id = Column(Integer, ForeignKey("mentorships.id"), nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, default="pending")
    deadline = Column(DateTime(timezone=True))
    comment = Column(Text)

    mentorship = relationship("Mentorship", back_populates="milestones")

class MentorSession(Base):
    __tablename__ = "mentor_sessions"

    id = Column(Integer, primary_key=True, index=True)
    mentorship_id = Column(Integer, ForeignKey("mentorships.id"), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    mentorship = relationship("Mentorship", back_populates="sessions")