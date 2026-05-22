from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.student import StudentProfile, Team
from app.schemas.student import StudentProfileCreate, StudentProfileResponse, TeamCreate, TeamResponse

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/profile", response_model=StudentProfileResponse)
def create_profile(data: StudentProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
    profile = StudentProfile(user_id=current_user.id, **data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/profile", response_model=StudentProfileResponse)
def get_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.patch("/profile", response_model=StudentProfileResponse)
def update_profile(data: StudentProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

@router.post("/teams", response_model=TeamResponse)
def create_team(data: TeamCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Create student profile first")
    team = Team(name=data.name, leader_id=profile.id)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team

@router.get("/teams/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team