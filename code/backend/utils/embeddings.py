# utils/embeddings.py

import logging
from sentence_transformers import SentenceTransformer

# Configure logging for embeddings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the embedding model
MODEL_NAME = 'all-MiniLM-L6-v2'  # You can choose another model if desired

try:
    logger.info(f"Loading embedding model '{MODEL_NAME}'...")
    embedding_model = SentenceTransformer(MODEL_NAME)
    EMBEDDING_DIMENSION = embedding_model.get_sentence_embedding_dimension()
    logger.info(f"Embedding model '{MODEL_NAME}' loaded successfully with dimension {EMBEDDING_DIMENSION}.")
except Exception as e:
    logger.error(f"Failed to load the embedding model '{MODEL_NAME}': {e}")
    raise e

def get_local_embedding(text):
    """
    Convert text to a vector using the local embedding model.
    """
    try:
        embedding = embedding_model.encode(text, convert_to_numpy=True).tolist()  # Convert numpy array to list
        return embedding
    except Exception as e:
        logger.error(f"Error generating embedding with local model: {e}")
        return None
