"""Database operations for Argo data."""

from typing import List, Dict, Any, Optional
from pymongo.collection import Collection
from app.database.connection import mongo_connection
from app.database.models import ArgoProfile
from app.config import settings
from app.utils.logging import get_logger

logger = get_logger(__name__)


class ArgoRepository:
    """Repository for Argo profile data operations."""
    
    def __init__(self):
        self._collection: Optional[Collection] = None
    
    @property
    def collection(self) -> Collection:
        """Get the profiles collection."""
        if not self._collection:
            self._collection = mongo_connection.get_collection(settings.COLLECTION_NAME)
        return self._collection
    
    def find_profiles(self, query: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Find profiles matching the given query.
        
        Args:
            query: MongoDB query dictionary
            limit: Maximum number of results to return
            
        Returns:
            List of matching profile documents
        """
        try:
            results = list(self.collection.find(query).limit(limit))
            logger.info(f"Found {len(results)} profiles matching query")
            return results
        except Exception as e:
            logger.error(f"Error finding profiles: {e}")
            raise
    
    def get_profile_by_id(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a single profile by its ID.
        
        Args:
            profile_id: Profile identifier (float_id_cycle_number)
            
        Returns:
            Profile document or None if not found
        """
        try:
            result = self.collection.find_one({"_id": profile_id})
            if result:
                logger.info(f"Found profile: {profile_id}")
            else:
                logger.info(f"Profile not found: {profile_id}")
            return result
        except Exception as e:
            logger.error(f"Error getting profile {profile_id}: {e}")
            raise
    
    def count_profiles(self, query: Optional[Dict[str, Any]] = None) -> int:
        """
        Count profiles matching the query.
        
        Args:
            query: MongoDB query dictionary (optional)
            
        Returns:
            Number of matching profiles
        """
        try:
            count = self.collection.count_documents(query or {})
            logger.info(f"Profile count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error counting profiles: {e}")
            raise
    
    def get_distinct_projects(self) -> List[str]:
        """
        Get list of distinct project names.
        
        Returns:
            List of unique project names
        """
        try:
            projects = self.collection.distinct("project_name")
            logger.info(f"Found {len(projects)} distinct projects")
            return projects
        except Exception as e:
            logger.error(f"Error getting distinct projects: {e}")
            raise

# Global repository instance
argo_repository = ArgoRepository()