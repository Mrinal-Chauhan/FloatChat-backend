"""Chat API routes."""

from fastapi import APIRouter, HTTPException, status
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.agent import get_agent_response
from app.utils.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Process a chat message and return the AI agent's response.
    
    Args:
        request: Chat request containing message and session_id
        
    Returns:
        ChatResponse with the agent's reply
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        logger.info(f"Received message for session {request.session_id}: {request.message}")
        
        # Call the agent logic
        agent_reply = get_agent_response(
            user_message=request.message, 
            session_id=request.session_id
        )
        
        return ChatResponse(response=agent_reply)
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )