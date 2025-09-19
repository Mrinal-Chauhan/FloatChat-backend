"""MongoDB connection management."""

from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from app.config import settings
from app.utils.logging import get_logger

logger = get_logger(__name__)

class MongoDBConnection:
    """MongoDB connection manager."""
    
    def __init__(self):
        self._client: Optional[MongoClient] = None
        self._database: Optional[Database] = None
        
    def connect(self) -> None:
        """Establish MongoDB connection."""
        try:
            self._client = MongoClient(settings.MONGODB_URI)
            self._database = self._client[settings.DB_NAME]
            # Test connection
            self._client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {settings.DB_NAME}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
            
    def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self._client:
            self._client.close()
            logger.info("Disconnected from MongoDB")
            
    @property
    def client(self) -> MongoClient:
        """Get MongoDB client."""
        if not self._client:
            self.connect()
        return self._client
        
    @property
    def database(self) -> Database:
        """Get database instance."""
        if not self._database:
            self.connect()
        return self._database
        
    def get_collection(self, collection_name: str) -> Collection:
        """Get a collection from the database."""
        return self.database[collection_name]

# Global connection instance
mongo_connection = MongoDBConnection()