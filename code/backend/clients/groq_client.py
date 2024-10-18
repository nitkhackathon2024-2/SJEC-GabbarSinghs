# clients/groq_client.py

import logging
from groq import Groq
from config import GROQ_API_KEY

# Configure logging for the Groq client
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_groq_client():
    """
    Initialize and return the Groq client.
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)
        logger.info("Groq client initialized successfully.")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Groq client: {e}")
        raise e
