"""AI Agent logic for handling user interactions and tool usage."""

import os
import json
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv

from app.core.tools.mongo_query import query_atlas
from app.utils.logging import get_logger
from app.config import settings

# Load environment variables
load_dotenv()
client = OpenAI(api_key=settings.OPENAI_API_KEY)
logger = get_logger(__name__)

# In-memory store for conversation histories. 
# In a production app, you'd use a database like Redis for this.
conversation_histories: Dict[str, List] = {}

# Define the tool for the OpenAI API
tools = [
    {
        "type": "function",
        "function": {
            "name": "query_atlas",
            "description": "Searches the Argo float database for profiles based on a user's question. Returns a list of matching profiles.",
            "parameters": {
                "type": "object",
                "properties": {
                    "natural_language_query": {
                        "type": "string",
                        "description": "A detailed, natural language question from the user that specifies what to search for. Example: 'Find profiles from the Argo-France project in March 2023'."
                    }
                },
                "required": ["natural_language_query"]
            }
        }
    }
]

def get_agent_response(user_message: str, session_id: str) -> str:
    """
    Manages the conversation and returns the agent's response.
    
    Args:
        user_message: The user's input message
        session_id: Unique identifier for the conversation session
        
    Returns:
        The agent's response as a string
    """
    logger.info(f"Processing message for session {session_id}: {user_message}")
    
    # Retrieve the history for this session, or start a new one
    if session_id not in conversation_histories:
        conversation_histories[session_id] = [
            {
                "role": "system", 
                "content": "You are FloatChat, an expert AI assistant for oceanographic ARGO float data. You have a tool to query the database. Do not make up data; if you don't know, use the tool. Keep your answers concise."
            }
        ]
    
    messages = conversation_histories[session_id]
    messages.append({"role": "user", "content": user_message})

    try:
        # First API call: Let the model decide if it needs to use a tool
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                if function_name == "query_atlas":
                    function_args = json.loads(tool_call.function.arguments)
                    query = function_args.get("natural_language_query")
                    function_response = query_atlas(natural_language_query=query)
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(function_response)
                    })
            
            # Second API call to get the final natural language response
            final_response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages
            )
            final_answer = final_response.choices[0].message.content
            messages.append({"role": "assistant", "content": final_answer})
            logger.info(f"Generated response with tool usage for session {session_id}")
            return final_answer
        else:
            # If no tool is needed, just get the response directly
            answer = response_message.content
            messages.append({"role": "assistant", "content": answer})
            logger.info(f"Generated direct response for session {session_id}")
            return answer
            
    except Exception as e:
        logger.error(f"Error generating agent response: {e}")
        return "I apologize, but I encountered an error while processing your request. Please try again."