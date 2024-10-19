# clients/mongo_client.py

import logging
from pymongo import MongoClient
from config import MONGODB_URI

# Configure logging for the MongoDB client
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_mongo_client():
    """
    Initialize and return the MongoDB client along with the database and collection.
    """
    try:
        client = MongoClient(MONGODB_URI, socketTimeoutMS=60000, connectTimeoutMS=60000)
        db = client['your_database_name']  # Replace with your actual DB name
        collection = db['your_collection_name']  # Replace with your actual collection name
        logger.info("MongoDB client initialized successfully.")
        return client, db, collection
    except Exception as e:
        logger.error(f"Failed to initialize MongoDB client: {e}")
        raise e
