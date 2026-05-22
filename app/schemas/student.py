from pydantic import BaseModel
from typing import List, Optional
from app.models.student import StudyProgram

class StudentProfileCreate(BaseModel):
    study_program: StudyProgram = None
    year: int = None
    skills: str = None
    gdpr_consent: bool = False

class StudentProfileResponse(BaseModel):
    id: int
    user_id: int
    study_program: StudyProgram = None
    year: int = None
    skills: str = None
    gdpr_consent: bool

    class Config:
        from_attributes = True

class TeamCreate(BaseModel):
    name: str

class TeamResponse(BaseModel):
    id: int
    name: str
    leader_id: int

    class Config:
        from_attributes = True