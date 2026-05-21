from pydantic import BaseModel
from datetime import datetime
from app.models.program import ProgramType, CallStatus

class ProgramCreate(BaseModel):
    type: ProgramType
    title: str
    description: str = None
    rules: dict = {}

class ProgramResponse(BaseModel):
    id: int
    type: ProgramType
    title: str
    description: str = None
    is_active: bool

    class Config:
        from_attributes = True

class CallCreate(BaseModel):
    program_id: int
    title: str
    description: str = None
    deadline: datetime = None
    criteria: dict = {}

class CallResponse(BaseModel):
    id: int
    program_id: int
    title: str
    description: str = None
    status: CallStatus
    deadline: datetime = None

    class Config:
        from_attributes = True