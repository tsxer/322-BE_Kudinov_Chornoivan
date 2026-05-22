from pydantic import BaseModel

class OrganizationCreate(BaseModel):
    name: str
    ico: str = None
    sector: str = None
    contact_email: str = None
    description: str = None

class OrganizationResponse(BaseModel):
    id: int
    name: str
    ico: str = None
    sector: str = None
    contact_email: str = None
    description: str = None

    class Config:
        from_attributes = True