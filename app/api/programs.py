from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User, UserRole
from app.models.program import Program, Call
from app.schemas.program import ProgramCreate, ProgramResponse, CallCreate, CallResponse
from typing import List

router = APIRouter(prefix="/programs", tags=["programs"])

@router.post("", response_model=ProgramResponse)
def create_program(data: ProgramCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.admin, UserRole.superadmin]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    program = Program(**data.model_dump())
    db.add(program)
    db.commit()
    db.refresh(program)
    return program

@router.get("", response_model=List[ProgramResponse])
def get_programs(db: Session = Depends(get_db)):
    return db.query(Program).filter(Program.is_active == True).all()

@router.get("/{program_id}", response_model=ProgramResponse)
def get_program(program_id: int, db: Session = Depends(get_db)):
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

@router.post("/calls", response_model=CallResponse)
def create_call(data: CallCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.admin, UserRole.superadmin]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    call = Call(**data.model_dump())
    db.add(call)
    db.commit()
    db.refresh(call)
    return call

@router.get("/calls/active", response_model=List[CallResponse])
def get_active_calls(db: Session = Depends(get_db)):
    return db.query(Call).filter(Call.status == "active").all()