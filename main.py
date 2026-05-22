from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.programs import router as programs_router
from app.api.applications import router as applications_router
from app.api.students import router as students_router
from app.api.organizations import router as organizations_router

app = FastAPI(
    title="NTI API",
    description="Centralny informacny system NTI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(programs_router)
app.include_router(applications_router)
app.include_router(students_router)
app.include_router(organizations_router)

@app.get("/")
def root():
    return {"message": "NTI API is running"}