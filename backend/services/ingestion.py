import requests
from typing import Dict, Any, List
import logging
from services.embedding import EmbeddingService
from services.vector_db import VectorDBService
from services.metadata_db import MetadataDBService
from utils.text_splitter import TextSplitter
from models.document import DocumentChunk

logger = logging.getLogger(__name__)


class IngestionService:
    """
    Service for document ingestion logic
    Handles fetching content from URLs, processing text, and storing embeddings
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_db_service = VectorDBService()
        self.metadata_db_service = MetadataDBService()
        self.text_splitter = TextSplitter()

    def ingest_from_url(self, url: str, doc_id: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Ingest document content from a URL
        """
        try:
            logger.info(f"Starting ingestion from URL: {url}")

            # Fetch content from URL
            response = requests.get(url)
            response.raise_for_status()

            content = response.text

            # Process the content
            result = self.ingest_content(content, doc_id, url, metadata or {})
            logger.info(f"Successfully ingested content from URL: {url}")
            return result

        except requests.RequestException as e:
            logger.error(f"Error fetching content from URL {url}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error ingesting content from URL {url}: {e}")
            raise

    def ingest_content(self, content: str, doc_id: str, source_url: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Ingest content from text directly
        """
        try:
            logger.info(f"Starting ingestion for document: {doc_id}")

            if not content or len(content.strip()) == 0:
                raise ValueError("Content is empty")

            # Split content into chunks
            chunks_data = self.text_splitter.split_text(
                text=content,
                doc_id=doc_id,
                source_url=source_url,
                metadata=metadata or {}
            )

            if not chunks_data:
                raise ValueError("No content to process after splitting")

            # Process each chunk: generate embedding and store
            chunk_ids = []
            for chunk_data in chunks_data:
                chunk_id = chunk_data['chunk_id']
                chunk_content = chunk_data['content']
                source_url = chunk_data['source_url']
                chunk_metadata = chunk_data['metadata']

                # Generate embedding for the chunk
                embedding = self.embedding_service.generate_single_embedding(chunk_content)

                # Create DocumentChunk model
                document_chunk = DocumentChunk(
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    content=chunk_content,
                    embedding=embedding,
                    source_url=source_url,
                    metadata=chunk_metadata
                )

                # Store in vector DB
                self.vector_db_service.upsert_chunk(document_chunk, embedding)

                # Store metadata in Postgres
                self.metadata_db_service.store_document_chunk(
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    content=chunk_content,
                    url=source_url,
                    metadata=chunk_metadata
                )

                chunk_ids.append(chunk_id)

            result = {
                "status": "success",
                "doc_id": doc_id,
                "chunks_processed": len(chunk_ids),
                "chunk_ids": chunk_ids
            }

            logger.info(f"Successfully processed {len(chunk_ids)} chunks for document {doc_id}")
            return result

        except Exception as e:
            logger.error(f"Error ingesting content for document {doc_id}: {e}")
            raise

    def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """
        Delete all chunks associated with a document
        """
        try:
            logger.info(f"Deleting document: {doc_id}")

            # Delete from vector DB
            self.vector_db_service.delete_document_chunks(doc_id)

            # Delete from metadata DB
            self.metadata_db_service.delete_document(doc_id)

            result = {
                "status": "success",
                "doc_id": doc_id,
                "message": f"Successfully deleted document {doc_id} and all its chunks"
            }

            logger.info(f"Successfully deleted document {doc_id}")
            return result

        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")
            raise