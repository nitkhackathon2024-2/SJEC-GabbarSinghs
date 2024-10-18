# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import asyncio  # For simulating processing time

app = FastAPI()

# Define CORS settings
origins = [
    "http://localhost",  # Your frontend's origin
    "http://localhost:3000",  # Example for React
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model
class TextRequest(BaseModel):
    raw_text: str

# Define the response model
class ProcessedResponse(BaseModel):
    processed_text: str
    embeddings: list  # Replace with actual data types as needed

@app.post("/api/process", response_model=ProcessedResponse)
async def process_text(request: TextRequest):
    try:
        raw_text = request.raw_text
        print(raw_text)
        # Simulate processing delay
        await asyncio.sleep(1)  # Remove or adjust in production

        # TODO: Replace the following with actual processing logic
       
        return "hi"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

# Configure logging for the main application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize Qdrant collection
    initialize_qdrant_collection()

    # # Replace this with your actual raw text input
    # raw_text = """
    # Your raw PDF extracted text goes here.
    # """

    # Reconstruct formatting using Groq LLM
    formatted_text = reconstruct_formatting(raw_text)
    if not formatted_text:
        logger.error("Failed to reconstruct formatting.")
        return

    # Store the formatted text in MongoDB and Qdrant
    store_data(formatted_text)

    # Fetch all vectors and generate a simplified knowledge graph
    documents = fetch_all_vectors()
    if documents:
        knowledge_graph_str = generate_summary_tree(documents)
        if knowledge_graph_str:
            logger.info(f"Knowledge Graph:\n{knowledge_graph_str}")

            # Store the knowledge graph in MongoDB under a different collection
            mongo_client, db, _ = get_mongo_client()
            knowledge_graph_collection = db['knowledge_graph']
            # Overwrite the existing document
            knowledge_graph_collection.replace_one(
                {},  # Filter to match all documents
                {"knowledge_graph": json.loads(knowledge_graph_str)},
                upsert=True
            )
            logger.info("Knowledge graph stored in MongoDB under 'knowledge_graph' collection.")
        else:
            logger.error("Failed to generate knowledge graph.")
    else:
        logger.error("No documents found in Qdrant.")

if __name__ == "__main__":
    main()
