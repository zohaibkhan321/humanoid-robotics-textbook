from pydantic import BaseModel
from typing import Optional, Dict, Any
from pydantic import field_validator


class Query(BaseModel):
    """
    Query - Request entity for user questions
    Fields:
    - query_text: string (the user's question)
    - selected_text: string (optional text selected by user, if any)
    - user_context: object (optional user-specific context)
    - session_id: string (optional session identifier for conversation history)
    """
    query_text: str
    selected_text: Optional[str] = None
    user_context: Optional[Dict[str, Any]] = {}
    session_id: Optional[str] = None

    @field_validator('query_text')
    @classmethod
    def validate_query_text(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Query text must be non-empty')
        if len(v) > 1000:
            raise ValueError('Query text must be under 1000 characters')
        return v

    @field_validator('selected_text')
    @classmethod
    def validate_selected_text(cls, v):
        if v is not None:
            if len(v) == 0:
                raise ValueError('Selected text must be non-empty when provided')
            if len(v) > 5000:
                raise ValueError('Selected text must be under 5000 characters')
        return v


class SearchQuery(BaseModel):
    """
    Model for search requests
    """
    query: str
    top_k: int = 5
    selected_text: Optional[str] = None


class EmbedRequest(BaseModel):
    """
    Request model for embedding documents
    """
    url: Optional[str] = None
    text: Optional[str] = None
    doc_id: str
    metadata: Dict[str, Any] = {}

    @field_validator('url', 'text', mode='before')
    @classmethod
    def validate_content_source(cls, v, info):
        # At least one of url or text must be provided
        values = info.data
        if info.field_name == 'url' and not v and not values.get('text'):
            raise ValueError('Either url or text must be provided')
        if info.field_name == 'text' and not v and not values.get('url'):
            raise ValueError('Either text or url must be provided')
        return v