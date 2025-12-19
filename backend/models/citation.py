from pydantic import BaseModel
from typing import Optional


class Citation(BaseModel):
    """
    Citation - Provenance entity for source attribution
    Fields:
    - url: string (source URL for the cited content)
    - chunk_id: string (identifier of the specific chunk)
    - similarity_score: float (relevance score of the citation)
    - text_preview: string (short preview of the cited text)
    """
    url: str
    chunk_id: str
    similarity_score: Optional[float] = None
    text_preview: Optional[str] = None