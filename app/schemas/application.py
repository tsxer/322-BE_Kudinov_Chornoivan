from pydantic import BaseModel
from datetime import datetime
from app.models.application import ApplicationStatus

class ApplicationCreate(BaseModel):
    call_id: int
    motivation: str = None

class ApplicationResponse(BaseModel):
    id: int
    call_id: int
    applicant_id: int
    status: ApplicationStatus
    motivation: str = None
    created_at: datetime

    class Config:
        from_attributes = True

class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus