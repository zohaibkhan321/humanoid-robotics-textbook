from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class DocumentChunk(BaseModel):
    """
    Document Chunk - Data entity representing a segment of book content
    Fields:
    - doc_id: string (unique document identifier)
    - chunk_id: string (unique chunk identifier within document)
    - content: string (the text content of the chunk)
    - embedding: vector (Cohere embedding vector for similarity search)
    - source_url: string (URL where the content originated)
    - metadata: object (additional information like page number, section, etc.)
    - created_at: datetime (timestamp when chunk was created)
    """
    doc_id: str
    chunk_id: str
    content: str
    embedding: Optional[list] = None  # Vector represented as a list of floats
    source_url: str
    metadata: Dict[str, Any] = {}
    created_at: datetime = datetime.now()

    class Config:
        # Allow arbitrary types for embedding vector
        arbitrary_types_allowed = True


class DocumentChunkCreate(BaseModel):
    """
    Request model for creating a new document chunk
    """
    doc_id: str
    content: str
    source_url: str
    metadata: Dict[str, Any] = {}


class DocumentChunkResponse(BaseModel):
    """
    Response model for document chunk operations
    """
    status: str
    doc_id: str
    chunks_processed: int
    chunk_ids: list[str]