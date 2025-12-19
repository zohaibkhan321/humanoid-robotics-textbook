from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging
from models.query import EmbedRequest
from models.document import DocumentChunkResponse
from services.embedding import EmbeddingService
from services.vector_db import VectorDBService
from services.metadata_db import MetadataDBService
from utils.text_splitter import TextSplitter
from config.settings import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
embedding_service = EmbeddingService()
vector_db_service = VectorDBService()
metadata_db_service = MetadataDBService()
text_splitter = TextSplitter()


@router.post("/embed", response_model=DocumentChunkResponse)
async def embed_document(request: EmbedRequest) -> Dict[str, Any]:
    """
    Generate and store embeddings for book content
    POST /api/v1/embed
    """
    try:
        logger.info(f"Processing embed request for doc_id: {request.doc_id}")

        # Validate that either URL or text is provided
        if not request.url and not request.text:
            raise HTTPException(status_code=400, detail="Either URL or text must be provided")

        # Get content - if URL is provided, fetch it; otherwise use the provided text
        content = request.text
        if request.url:
            # In a real implementation, you would fetch content from the URL
            # For now, we'll simulate this by assuming content is provided directly
            # or you would use a library like requests to fetch it
            logger.warning("URL fetching not implemented in this example, using text directly if provided")
            if not request.text:
                raise HTTPException(status_code=400, detail="Text content must be provided when URL is specified")

        # Split the content into chunks
        chunks_data = text_splitter.split_text(
            text=content,
            doc_id=request.doc_id,
            source_url=request.url or "unknown",
            metadata=request.metadata
        )

        if not chunks_data:
            raise HTTPException(status_code=422, detail="No content to process")

        # Process each chunk: generate embedding and store
        chunk_ids = []
        for chunk_data in chunks_data:
            chunk_id = chunk_data['chunk_id']
            chunk_content = chunk_data['content']
            source_url = chunk_data['source_url']
            metadata = chunk_data['metadata']

            # Generate embedding for the chunk
            embedding = embedding_service.generate_single_embedding(chunk_content)

            # Create DocumentChunk model
            from models.document import DocumentChunk
            document_chunk = DocumentChunk(
                doc_id=request.doc_id,
                chunk_id=chunk_id,
                content=chunk_content,
                embedding=embedding,
                source_url=source_url,
                metadata=metadata
            )

            # Store in vector DB
            vector_db_service.upsert_chunk(document_chunk, embedding)

            # Store metadata in Postgres
            metadata_db_service.store_document_chunk(
                doc_id=request.doc_id,
                chunk_id=chunk_id,
                content=chunk_content,
                url=source_url,
                metadata=metadata
            )

            chunk_ids.append(chunk_id)

        response = DocumentChunkResponse(
            status="success",
            doc_id=request.doc_id,
            chunks_processed=len(chunk_ids),
            chunk_ids=chunk_ids
        )

        logger.info(f"Successfully processed {len(chunk_ids)} chunks for document {request.doc_id}")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing embed request: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")