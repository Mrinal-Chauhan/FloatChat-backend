"""MongoDB query tool for AI agent."""

import os
import json
from typing import List, Dict, Any
from pymongo import MongoClient
from openai import OpenAI
from dotenv import load_dotenv
from app.config import settings

from app.utils.logging import get_logger

# Load environment variables from .env file
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
mongo_client = MongoClient(settings.MONGODB_URI)
db = mongo_client[settings.DB_NAME]
collection = db[settings.COLLECTION_NAME]

logger = get_logger(__name__)

# The schema of our MongoDB documents, for the LLM's context
MONGO_SCHEMA = """
{
  "_id": "<float_id>_<cycle_number>",
  "float_id": int,
  "cycle_number": int,
  "time": datetime,
  "project_name": str,
  "location": { "type": "Point", "coordinates": [longitude, latitude] },
  "measurements": int # Number of measurement entries in the profile
}
"""

def query_atlas(natural_language_query: str) -> List[Dict[str, Any]]:
    """
    Query the Argo atlas database using natural language.
    
    Args:
        natural_language_query: Natural language description of what to search for
        
    Returns:
        List of matching documents (summarized)
    """
    logger.info(f"🛠️ Tool received query: '{natural_language_query}'")
    
    # Prompt for converting natural language to MQL
    prompt = f"""
    Based on the following MongoDB document schema, your task is to translate the user's natural language query into a valid MQL filter.
    
    Schema:
    {MONGO_SCHEMA}

    - The 'time' field is a datetime object. For date queries, use ISODate format. For example, for March 2023, the query on 'time' would be {{ "$gte": ISODate("2023-03-01T00:00:00Z"), "$lt": ISODate("2023-04-01T00:00:00Z") }}.
    
    - **IMPORTANT FOR LOCATION QUERIES**: The 'location' field is a GeoJSON Point. For geospatial queries, use the `$near` operator. The coordinates are in [longitude, latitude] order. **Always include a reasonable search radius, like 1000 meters, for `$maxDistance` unless the user specifies otherwise.** For example: {{ "location": {{ "$near": {{ "$geometry": {{ "type": "Point", "coordinates": [lon, lat] }}, "$maxDistance": 1000 }} }} }}

    - Always return ONLY the JSON filter object, with no other text or explanation.

    Example 1:
    User query: "Find the profile for float 5906527 with cycle number 94"
    MQL: {{ "_id": "5906527_94" }}

    Example 2:
    User query: "Show me profiles from the 'Argo-France' project"
    MQL: {{ "project_name": "Argo-France" }}
    
    Now, translate the following user query.
    User query: "{natural_language_query}"
    MQL:
    """
    
    try:
        response = openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        mql_string = response.choices[0].message.content
        logger.info(f"🧠 Generated MQL: {mql_string}")

        # Clean the MQL string to remove markdown formatting (```json ... ```)
        if "```" in mql_string:
            # Find the start and end of the JSON object
            start_index = mql_string.find('{')
            end_index = mql_string.rfind('}')
            if start_index != -1 and end_index != -1:
                mql_string = mql_string[start_index : end_index + 1]
        
        mql_query = json.loads(mql_string)
        
        # Execute the query
        full_results = list(collection.find(mql_query).limit(10))
        
        # Summarize results to avoid overwhelming the AI
        summarized_results = []
        for doc in full_results:
            summary = {
                "_id": str(doc.get("_id")),
                "float_id": doc.get("float_id"),
                "cycle_number": doc.get("cycle_number"),
                "time": doc.get("time").isoformat() if doc.get("time") else None,
                "project_name": doc.get("project_name"),
                "measurement_count": len(doc.get("measurements", []))
            }
            summarized_results.append(summary)

        logger.info(f"🔍 Found {len(summarized_results)} documents. Returning summary to agent.")
        return summarized_results

    except json.JSONDecodeError as e:
        logger.error(f"🔴 JSON DECODE ERROR: {e} - on string: '{mql_string}'")
        return [{"error": "Failed to generate valid MQL JSON from the language model."}]
    except Exception as e:
        logger.error(f"🔴 DATABASE/OTHER ERROR: {e}")
        return [{"error": f"An error occurred while querying MongoDB: {e}"}]