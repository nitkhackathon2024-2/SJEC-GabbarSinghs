# clients/qdrant_client.py

import logging
from qdrant_client import QdrantClient
from config import QDRANT_URL, QDRANT_API_KEY

# Configure logging for the Qdrant client
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_qdrant_client():
    """
    Initialize and return the Qdrant client.
    """
    try:
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY if QDRANT_API_KEY else None
        )
        logger.info(f"Connected to Qdrant at {QDRANT_URL}")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {e}")
        raise e
