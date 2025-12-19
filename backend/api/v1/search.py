from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List
import logging
from models.query import SearchQuery
from services.embedding import EmbeddingService
from services.vector_db import VectorDBService
from config.settings import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
embedding_service = EmbeddingService()
vector_db_service = VectorDBService()


@router.post("/search")
async def search_content(request: SearchQuery) -> Dict[str, Any]:
    """
    Search for relevant content based on query
    POST /api/v1/search
    """
    try:
        logger.info(f"Processing search request for query: {request.query[:50]}...")

        # Validate query length
        if len(request.query) > settings.max_query_length:
            raise HTTPException(status_code=400, detail=f"Query exceeds maximum length of {settings.max_query_length} characters")

        # Generate embedding for the query
        query_embedding = embedding_service.generate_query_embedding(request.query)

        # Search in vector database
        search_results = vector_db_service.search_chunks(
            query_embedding=query_embedding,
            top_k=request.top_k,
            selected_text=request.selected_text
        )

        # If selected_text is provided, we need to handle it specially
        if request.selected_text:
            # In selected text mode, we don't return vector search results
            # Instead, we return the selected text as context
            # For now, return empty results - the answer endpoint will handle this
            logger.info("Selected text mode: returning empty vector search results")
            search_results = []

        response = {
            "query": request.query,
            "results": search_results
        }

        logger.info(f"Search completed, found {len(search_results)} results")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing search request: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")