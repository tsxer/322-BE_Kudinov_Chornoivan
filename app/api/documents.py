from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.cloudinary import upload_file
from app.models.user import User
from app.models.application import Application
from pydantic import BaseModel

router = APIRouter(prefix="/documents", tags=["documents"])

ALLOWED_TYPES = ["application/pdf", "image/jpeg", "image/png", "application/msword",
                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]

class DocumentResponse(BaseModel):
    application_id: int
    file_url: str
    filename: str

@router.post("/{application_id}", response_model=DocumentResponse)
async def upload_document(
    application_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if application.applicant_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your application")
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="File type not allowed. Use PDF, JPEG, PNG or DOCX")
    
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Max 10MB")
    
    url = upload_file(contents, f"app_{application_id}_{file.filename}", folder="nti/documents")
    
    return {
        "application_id": application_id,
        "file_url": url,
        "filename": file.filename
    }