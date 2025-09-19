"""Health check API routes."""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/")
def read_root():
    """Root endpoint with basic API information."""
    return {
        "status": "FloatChat API is running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "FloatChat API",
        "timestamp": datetime.now().isoformat()
    }