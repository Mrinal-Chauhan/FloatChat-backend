"""
FloatChat Application Entry Point

This script serves as the main entry point for the FloatChat application.
It starts the FastAPI server using uvicorn.
"""

import uvicorn
from app.main import app

def main():
    """Start the FloatChat application server."""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()
