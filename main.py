from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.auth import router as auth_router
from app.api.programs import router as programs_router
from app.api.applications import router as applications_router
from app.api.students import router as students_router
from app.api.organizations import router as organizations_router
from app.api.evaluations import router as evaluations_router
from app.api.mentorships import router as mentorships_router
from app.api.documents import router as documents_router
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from app.core.limiter import limiter

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

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors_map = {err["loc"][-1]: err["msg"] for err in exc.errors()}
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation failed",
            "errors": errors_map
        }
    )

app.include_router(auth_router)
app.include_router(programs_router)
app.include_router(applications_router)
app.include_router(students_router)
app.include_router(organizations_router)
app.include_router(evaluations_router)
app.include_router(mentorships_router)
app.include_router(documents_router)

@app.get("/")
def root():
    return {"message": "NTI API is running"}