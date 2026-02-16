from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db

router = APIRouter(tags=["Health"])


@router.get("/health", tags=["Health"])
def health():
    """Basic liveness check. Returns service status and environment."""
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "version": settings.API_VERSION,
    }


@router.get("/health/db", tags=["Health"])
def health_db(db: Session = Depends(get_db)):
    """Readiness check that verifies the database is reachable."""
    try:
        # simple check
        db.execute(text("SELECT 1"))
        return {"status": "database is up and running."}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
