from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User, UserRole
from app.models.audit import AuditEvent
from app.models.application import Application

router = APIRouter(prefix="/admin", tags=["admin"])

class AuditResponse(BaseModel):
    id: int
    actor_id: int = None
    action: str
    resource_type: str = None
    resource_id: int = None
    ip_address: str = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class StatsResponse(BaseModel):
    total_users: int
    total_applications: int
    applications_by_status: dict

@router.get("/audit", response_model=List[AuditResponse])
def get_audit_log(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.admin, UserRole.superadmin]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return db.query(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(100).all()

@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.admin, UserRole.superadmin]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    from app.models.user import User as UserModel
    total_users = db.query(UserModel).count()
    total_applications = db.query(Application).count()
    
    from app.models.application import ApplicationStatus
    by_status = {}
    for status in ApplicationStatus:
        count = db.query(Application).filter(Application.status == status).count()
        by_status[status.value] = count
    
    return {
        "total_users": total_users,
        "total_applications": total_applications,
        "applications_by_status": by_status
    }