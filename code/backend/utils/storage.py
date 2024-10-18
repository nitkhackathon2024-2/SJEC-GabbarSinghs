# utils/storage.py

import logging
import uuid
from pymongo.errors import PyMongoError
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from clients import get_mongo_client, get_qdrant_client
from utils.embeddings import get_local_embedding, EMBEDDING_DIMENSION

# Configure logging for storage
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
mongo_client, db, collection = get_mongo_client()
qdrant_client = get_qdrant_client()

# Define Qdrant collection name and embedding dimensions
QDRANT_COLLECTION_NAME = "pdf_texts"

def initialize_qdrant_collection():
    """
    Create Qdrant collection if it doesn't exist.
    """
    try:
        existing_collections = qdrant_client.get_collections()
        collection_names = [col.name for col in existing_collections.collections]
        if QDRANT_COLLECTION_NAME not in collection_names:
            qdrant_client.create_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIMENSION,
                    distance=Distance.COSINE  # Choose distance metric based on your use case
                )
            )
            logger.info(f"Created Qdrant collection '{QDRANT_COLLECTION_NAME}'")
        else:
            logger.info(f"Qdrant collection '{QDRANT_COLLECTION_NAME}' already exists")
    except Exception as e:
        logger.error(f"Error creating/accessing Qdrant collection: {e}")
        raise e

def store_data(formatted_text):
    """
    Store the formatted text in MongoDB and Qdrant Vector DB.
    """
    try:
        # Get the maximum sequence length of the embedding model
        max_seq_length = 512  # Default to 512; adjust if your model supports dynamic lengths
        logger.info(f"Embedding model max sequence length: {max_seq_length}")

        # Split formatted_text into smaller chunks based on max_seq_length
        tokens = formatted_text.split()
        chunks = []
        current_chunk = []

        for word in tokens:
            current_chunk.append(word)
            # Approximate length by number of tokens
            if len(current_chunk) >= max_seq_length - 10:  # Leave some buffer
                chunks.append(' '.join(current_chunk))
                current_chunk = []
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        logger.info(f"Total chunks created: {len(chunks)}")

        mongo_ids = []
        vector_ids = []

        for chunk in chunks:
            # Insert each chunk as a document in MongoDB
            document = {
                "formatted_text": chunk
            }
            mongo_result = collection.insert_one(document)
            mongo_id_str = str(mongo_result.inserted_id)
            logger.info(f"Formatted text chunk inserted into MongoDB with _id: {mongo_id_str}")
            mongo_ids.append(mongo_id_str)

            # Generate embedding for the chunk
            vector = get_local_embedding(chunk)
            if not vector:
                logger.error("Failed to generate embedding for the formatted text chunk.")
                continue

            # Validate embedding dimension
            if len(vector) != EMBEDDING_DIMENSION:
                logger.error(f"Embedding dimension mismatch: expected {EMBEDDING_DIMENSION}, got {len(vector)}")
                continue

            # Generate a UUID for Qdrant vector ID
            vector_id = str(uuid.uuid4())
            vector_ids.append(vector_id)

            # Upsert into Qdrant
            point = PointStruct(
                id=vector_id,
                vector=vector,
                payload={
                    "mongo_id": mongo_id_str,
                    "source": "ingest.py",
                    "formatted_text": chunk  # Include formatted_text in payload
                }
            )
            qdrant_client.upsert(
                collection_name=QDRANT_COLLECTION_NAME,
                points=[point]
            )
            logger.info(f"Vector upserted into Qdrant with ID: {vector_id}")

    except PyMongoError as e:
        logger.error(f"MongoDB insertion error: {e}")
        raise e
    except Exception as e:
        logger.error(f"Qdrant upsert error: {e}")
        raise e

def fetch_all_vectors():
    """
    Fetch all vectors from Qdrant Vector DB along with their metadata.
    """
    try:
        logger.info("Fetching all vectors from Qdrant...")

        # Initialize variables for pagination
        vectors = []
        page_size = 100  # Adjust based on your data size
        offset = None

        while True:
            scroll_result, next_page_offset = qdrant_client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                limit=page_size,
                offset=offset,
                with_payload=True,
                with_vectors=False,  # No need to fetch vectors themselves
            )

            if isinstance(scroll_result, list):
                for point in scroll_result:
                    vectors.append(point.payload.get("formatted_text", ""))
            else:
                logger.error("Unexpected scroll result format. Expected a list of points.")
                break

            # Check if there are more pages to scroll through
            if next_page_offset is None:
                break
            else:
                offset = next_page_offset

        logger.info(f"Fetched a total of {len(vectors)} vectors from Qdrant.")
        return vectors

    except Exception as e:
        logger.error(f"Error fetching vectors from Qdrant: {e}")
        return []
