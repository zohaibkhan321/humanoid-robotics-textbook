from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional, Dict, Any
from config.settings import settings
from models.document import DocumentChunk
import uuid
import logging

logger = logging.getLogger(__name__)


# Global variable to store the singleton instance
_vector_db_service_instance = None

class VectorDBService:
    """
    Service for interacting with Qdrant vector database
    """
    def __new__(cls):
        global _vector_db_service_instance
        if _vector_db_service_instance is None:
            _vector_db_service_instance = super().__new__(cls)
            # Initialize on first creation
            _vector_db_service_instance._client = None
            _vector_db_service_instance.collection_name = settings.collection_name

            # Store configuration for later initialization
            _vector_db_service_instance.qdrant_local_path = settings.qdrant_local_path
            _vector_db_service_instance.qdrant_url = settings.qdrant_url
            _vector_db_service_instance.qdrant_api_key = settings.qdrant_api_key
        return _vector_db_service_instance

    def __init__(self):
        # Prevent re-initialization of instance variables
        pass

    @property
    def client(self):
        """Lazy initialization of Qdrant client"""
        if self._client is None:
            # Initialize Qdrant client - use local storage if path is specified
            if self.qdrant_local_path:
                # Use local Qdrant storage
                self._client = QdrantClient(path=self.qdrant_local_path)
            elif self.qdrant_api_key:
                # Use remote Qdrant with API key
                self._client = QdrantClient(
                    url=self.qdrant_url,
                    api_key=self.qdrant_api_key,
                    prefer_grpc=True
                )
            else:
                # Use remote Qdrant without API key (for local server)
                self._client = QdrantClient(url=self.qdrant_url)

            # Initialize the collection if it doesn't exist
            self._initialize_collection()
        return self._client

    def _initialize_collection(self):
        """
        Initialize the Qdrant collection for document chunks
        """
        try:
            # Check if collection exists
            self._client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self._client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # Cohere embedding dimension
                    distance=models.Distance.COSINE
                )
            )

            # Create payload index for doc_id to speed up filtering
            self._client.create_payload_index(
                collection_name=self.collection_name,
                field_name="doc_id",
                field_schema=models.PayloadSchemaType.KEYWORD
            )

    def upsert_chunk(self, chunk: DocumentChunk, embedding: List[float]):
        """
        Upsert a document chunk with its embedding into Qdrant
        """
        points = [
            models.PointStruct(
                id=uuid.uuid5(uuid.NAMESPACE_DNS, chunk.chunk_id).int,
                vector=embedding,
                payload={
                    "doc_id": chunk.doc_id,
                    "chunk_id": chunk.chunk_id,
                    "content": chunk.content,
                    "source_url": chunk.source_url,
                    "metadata": chunk.metadata,
                    "created_at": chunk.created_at.isoformat()
                }
            )
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search_chunks(self, query_embedding: List[float], top_k: int = 5, doc_ids: Optional[List[str]] = None, selected_text: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for similar chunks based on embedding
        If selected_text is provided, returns empty results as search should be constrained to that text only
        """
        if selected_text:
            # When selected text is provided, we don't search in the vector DB
            # Instead, the agent service will handle this by using only the selected text as context
            logger.info("Selected text provided, returning empty search results for vector DB")
            return []

        search_filter = None
        if doc_ids:
            search_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="doc_id",
                        match=models.MatchAny(any=doc_ids)
                    )
                ]
            )

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=top_k,
            query_filter=search_filter,
            with_payload=True
        )

        # Format results - QueryResponse object has points attribute
        formatted_results = []
        for result in results.points:
            formatted_results.append({
                "chunk_id": result.payload["chunk_id"],
                "content": result.payload["content"],
                "url": result.payload["source_url"],
                "similarity_score": result.score,
                "metadata": result.payload["metadata"]
            })

        logger.info(f"Found {len(formatted_results)} similar chunks for query")
        return formatted_results

    def delete_document_chunks(self, doc_id: str):
        """
        Delete all chunks associated with a document
        """
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="doc_id",
                            match=models.MatchValue(value=doc_id)
                        )
                    ]
                )
            )
        )

    def get_chunk_by_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific chunk by its ID
        """
        # Convert chunk_id to UUID
        point_id = uuid.uuid5(uuid.NAMESPACE_DNS, chunk_id).int

        results = self.client.retrieve(
            collection_name=self.collection_name,
            ids=[point_id],
            with_payload=True,
            with_vectors=False
        )

        if results:
            result = results[0]
            return {
                "chunk_id": result.payload["chunk_id"],
                "content": result.payload["content"],
                "url": result.payload["source_url"],
                "metadata": result.payload["metadata"],
                "created_at": result.payload["created_at"]
            }

        return None