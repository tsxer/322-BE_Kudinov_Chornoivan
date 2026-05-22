from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User, UserRole
from app.models.mentorship import Mentorship, Milestone, MentorSession

router = APIRouter(prefix="/mentorships", tags=["mentorships"])

class MentorshipCreate(BaseModel):
    application_id: int
    mentor_id: int

class MentorshipResponse(BaseModel):
    id: int
    application_id: int
    mentor_id: int

    class Config:
        from_attributes = True

class MilestoneCreate(BaseModel):
    mentorship_id: int
    title: str
    deadline: str = None

class MilestoneResponse(BaseModel):
    id: int
    mentorship_id: int
    title: str
    status: str

    class Config:
        from_attributes = True

class SessionCreate(BaseModel):
    mentorship_id: int
    notes: str = None

class SessionResponse(BaseModel):
    id: int
    mentorship_id: int
    notes: str = None

    class Config:
        from_attributes = True

@router.post("", response_model=MentorshipResponse)
def create_mentorship(data: MentorshipCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.admin, UserRole.superadmin]:
        raise HTTPException(status_code=403, detail="Only admin can assign mentors")
    mentorship = Mentorship(**data.model_dump())
    db.add(mentorship)
    db.commit()
    db.refresh(mentorship)
    return mentorship

@router.post("/milestones", response_model=MilestoneResponse)
def create_milestone(data: MilestoneCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    milestone = Milestone(title=data.title, mentorship_id=data.mentorship_id)
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    return milestone

@router.patch("/milestones/{milestone_id}/status", response_model=MilestoneResponse)
def update_milestone(milestone_id: int, status: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    milestone.status = status
    db.commit()
    db.refresh(milestone)
    return milestone

@router.post("/sessions", response_model=SessionResponse)
def create_session(data: SessionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session = MentorSession(**data.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session