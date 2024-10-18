# config/settings.py

import os
import logging
from dotenv import load_dotenv

# Configure logging for the config module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MONGODB_URI = os.getenv('MONGODB_URI')
QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY', '')  # Optional for local setups

# Validate environment variables
REQUIRED_VARS = ['GROQ_API_KEY', 'MONGODB_URI', 'QDRANT_URL']
missing_vars = [var for var in REQUIRED_VARS if not os.getenv(var)]

if missing_vars:
    error_message = f"Missing environment variables: {', '.join(missing_vars)}. Please check your .env file."
    logger.error(error_message)
    raise ValueError(error_message)

logger.info("All required environment variables are loaded successfully.")
