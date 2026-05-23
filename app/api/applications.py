import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User, UserRole
from app.models.application import Application, ApplicationStatus
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationStatusUpdate
from app.services.email_service import send_application_status_email


router = APIRouter(prefix="/applications", tags=["applications"])

ALLOWED_TRANSITIONS = {
    ApplicationStatus.draft: [ApplicationStatus.submitted],
    ApplicationStatus.submitted: [ApplicationStatus.formal_check, ApplicationStatus.rejected],
    ApplicationStatus.formal_check: [ApplicationStatus.in_review, ApplicationStatus.needs_info, ApplicationStatus.rejected],
    ApplicationStatus.in_review: [ApplicationStatus.approved, ApplicationStatus.needs_info, ApplicationStatus.rejected],
    ApplicationStatus.needs_info: [ApplicationStatus.in_review, ApplicationStatus.rejected],
    ApplicationStatus.approved: [ApplicationStatus.active],
    ApplicationStatus.active: [ApplicationStatus.archived],
}

@router.post("", response_model=ApplicationResponse)
def create_application(data: ApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    app = Application(
        call_id=data.call_id,
        applicant_id=current_user.id,
        motivation=data.motivation
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

@router.get("", response_model=List[ApplicationResponse])
def get_applications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role in [UserRole.admin, UserRole.superadmin, UserRole.commission]:
        return db.query(Application).all()
    return db.query(Application).filter(Application.applicant_id == current_user.id).all()

@router.get("/{app_id}", response_model=ApplicationResponse)
def get_application(app_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if application.applicant_id != current_user.id and current_user.role not in [UserRole.admin, UserRole.superadmin, UserRole.commission]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return application

@router.patch("/{app_id}/status", response_model=ApplicationResponse)
async def update_status(app_id: int, data: ApplicationStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    allowed = ALLOWED_TRANSITIONS.get(application.status, [])
    if data.status not in allowed:
        raise HTTPException(status_code=400, detail=f"Cannot transition from {application.status} to {data.status}")
    application.status = data.status
    db.commit()
    db.refresh(application)
    asyncio.create_task(send_application_status_email(
        application.applicant.email,
        data.status.value,
        app_id
    ))
    return application