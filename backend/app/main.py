import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from backend.app.core.config import settings
from backend.app.core.database import engine, Base
from backend.app.api.v1.router import api_router
from backend.app.models.profile import PatientProfile  # Ensure model is registered

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("medassist.backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Attempt to initialize database tables on startup if PostgreSQL connection succeeds
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified/created successfully.")
    except Exception as e:
        logger.warning(
            f"Could not automatically create database tables on startup ({e}). "
            "Please ensure PostgreSQL is running and credentials in .env are correct."
        )
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="MedAssist AI - Patient Profile Management Module (FastAPI & PostgreSQL)",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom validation error handler for clear, structured error responses
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err.get("loc", []) if loc != "body")
        errors.append({
            "field": field,
            "message": err.get("msg", "Invalid value"),
            "type": err.get("type", "value_error"),
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Input validation failed. Please check the submitted fields.",
            "errors": errors,
        },
    )


# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"], summary="System Health Check")
def health_check():
    return {
        "status": "healthy",
        "service": "MedAssist AI - Patient Profile Management API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to MedAssist AI API",
        "docs_url": "/docs",
        "profile_endpoint": f"{settings.API_V1_STR}/profile/me",
    }
