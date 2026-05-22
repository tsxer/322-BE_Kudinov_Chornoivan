import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from app.core.database import Base

class StudyProgram(str, enum.Enum):
    software = "software"
    ai = "ai"
    web = "web"
    gamedev = "gamedev"
    iot = "iot"

team_members = Table(
    "team_members",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("teams.id")),
    Column("student_id", Integer, ForeignKey("student_profiles.id"))
)

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    study_program = Column(Enum(StudyProgram))
    year = Column(Integer)
    skills = Column(String)
    cv_url = Column(String)
    gdpr_consent = Column(Boolean, default=False)

    user = relationship("User", back_populates="student_profile")
    teams = relationship("Team", secondary=team_members, back_populates="members")

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    leader_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)

    leader = relationship("StudentProfile", foreign_keys=[leader_id])
    members = relationship("StudentProfile", secondary=team_members, back_populates="teams")