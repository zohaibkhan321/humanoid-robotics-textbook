from pydantic import BaseModel
from typing import List, Optional
from .citation import Citation
from datetime import datetime


class Response(BaseModel):
    """
    Response - Result entity for chatbot answers
    Fields:
    - answer: string (the chatbot's response)
    - citations: array of citation objects (sources used in the answer)
    - confidence_score: float (confidence level of the response)
    - query_id: string (reference to the original query)
    - timestamp: datetime (when the response was generated)
    """
    query: str  # original query
    answer: str  # the chatbot's response
    citations: List[Citation] = []  # citations used in the answer
    confidence_score: Optional[float] = None  # confidence level of the response
    query_id: Optional[str] = None  # reference to the original query
    timestamp: datetime = datetime.now()  # when the response was generated


class EmbedResponse(BaseModel):
    """
    Response for embed endpoint
    """
    status: str
    doc_id: str
    chunks_processed: int
    chunk_ids: List[str]


class SearchResponse(BaseModel):
    """
    Response for search endpoint
    """
    query: str
    results: List[dict]  # Contains chunk_id, content, url, similarity_score, metadata


class InsufficientContextResponse(BaseModel):
    """
    Response when context is insufficient
    """
    status: str = "insufficient_context"
    message: str
    selected_text_provided: bool = False