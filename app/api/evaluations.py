from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User, UserRole
from app.models.evaluation import Evaluation

router = APIRouter(prefix="/evaluations", tags=["evaluations"])

class EvaluationCreate(BaseModel):
    application_id: int
    score: float
    comment: str = None
    decision: str = None

class EvaluationResponse(BaseModel):
    id: int
    application_id: int
    evaluator_id: int
    score: float = None
    comment: str = None
    decision: str = None

    class Config:
        from_attributes = True

@router.post("", response_model=EvaluationResponse)
def create_evaluation(data: EvaluationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.commission, UserRole.admin, UserRole.superadmin]:
        raise HTTPException(status_code=403, detail="Only commission can evaluate")
    evaluation = Evaluation(evaluator_id=current_user.id, **data.model_dump())
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation

@router.get("/application/{app_id}", response_model=List[EvaluationResponse])
def get_evaluations(app_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.commission, UserRole.admin, UserRole.superadmin]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return db.query(Evaluation).filter(Evaluation.application_id == app_id).all()