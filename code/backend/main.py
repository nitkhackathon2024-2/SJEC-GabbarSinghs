# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import json
from utils import (
    reconstruct_formatting,
    store_data,
    fetch_all_vectors,
    generate_summary_tree,
    initialize_qdrant_collection
)
from clients import get_mongo_client, get_qdrant_client

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS
origins = [
    "http://localhost:3000",  # Frontend origin
    # Add other allowed origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Or ["*"] for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    mongo_client, db, collection = get_mongo_client()
    logger.info("MongoDB client initialized in main.py successfully.")
except Exception as e:
    logger.error(f"Failed to initialize MongoDB client in main.py: {e}")
    raise e

# Define request and response models
class TextRequest(BaseModel):
    raw_text: str

class KnowledgeGraphResponse(BaseModel):
    knowledge_graph: dict

# Define your endpoint
@app.post("/api/process", response_model=KnowledgeGraphResponse)
async def process_text(request: TextRequest):
    try:
        initialize_qdrant_collection()

        raw_text = request.raw_text

        formatted_text = reconstruct_formatting(raw_text)
        if not formatted_text:
            logger.error("Failed to reconstruct formatting.")
            raise HTTPException(status_code=500, detail="Formatting reconstruction failed.")

        store_data(formatted_text)

        # Fetch all vectors and generate a simplified knowledge graph
        documents = fetch_all_vectors()
        if documents:
            # Fetch existing knowledge graph from MongoDB (assuming you store it there)
            existing_graph = db['knowledge_graph'].find_one({"_id": "main_graph"})
            existing_graph_data = existing_graph['data'] if existing_graph else {}

            # Generate new summary tree by merging with existing graph
            knowledge_graph_str = generate_summary_tree(documents, existing_graph_data)
            if knowledge_graph_str:
                # Update the stored knowledge graph
                db['knowledge_graph'].update_one(
                    {"_id": "main_graph"},
                    {"$set": {"data": json.loads(knowledge_graph_str)}},
                    upsert=True
                )
                logger.info("Knowledge Graph updated successfully.")
                return KnowledgeGraphResponse(knowledge_graph=json.loads(knowledge_graph_str))
            else:
                logger.error("Failed to generate knowledge graph.")
                raise HTTPException(status_code=500, detail="Knowledge graph generation failed.")
        else:
            logger.error("No documents found in Qdrant.")
            raise HTTPException(status_code=500, detail="No documents found for processing.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))