"""Chat request and response schemas."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., description="User's message", min_length=1, max_length=2000)
    session_id: str = Field(..., description="Session identifier", min_length=1, max_length=100)
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Show me profiles from the Argo-France project in March 2023",
                "session_id": "user123_session456"
            }
        }


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str = Field(..., description="AI agent's response")
    
    class Config:
        schema_extra = {
            "example": {
                "response": "I found 15 profiles from the Argo-France project in March 2023. Here are the details..."
            }
        }