from typing import List, Dict, Any
import logging
from models.citation import Citation
from services.vector_db import VectorDBService
from services.metadata_db import MetadataDBService

logger = logging.getLogger(__name__)


class CitationService:
    """
    Service for citation generation and validation
    Handles creating, formatting, and validating citations for answers
    """

    def __init__(self):
        self.vector_db_service = VectorDBService()
        self.metadata_db_service = MetadataDBService()

    def generate_citations_from_chunks(self, chunks: List[Dict[str, Any]]) -> List[Citation]:
        """
        Generate citations from search result chunks
        """
        citations = []
        for chunk in chunks:
            if chunk.get("url") and chunk.get("chunk_id"):
                citation = Citation(
                    url=chunk["url"],
                    chunk_id=chunk["chunk_id"],
                    similarity_score=chunk.get("similarity_score", 0.0),
                    text_preview=chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"]
                )
                citations.append(citation)

        logger.info(f"Generated {len(citations)} citations from {len(chunks)} chunks")
        return citations

    def validate_citations(self, citations: List[Citation]) -> List[Citation]:
        """
        Validate that all citations reference valid chunks in the database
        """
        validated_citations = []
        for citation in citations:
            # Try to retrieve the chunk to verify it exists
            chunk = self.vector_db_service.get_chunk_by_id(citation.chunk_id)
            if chunk:
                validated_citations.append(citation)
            else:
                logger.warning(f"Invalid citation: chunk {citation.chunk_id} not found in database")

        logger.info(f"Validated {len(validated_citations)} out of {len(citations)} citations")
        return validated_citations

    def format_citations(self, citations: List[Citation]) -> List[Dict[str, Any]]:
        """
        Format citations for response
        """
        formatted_citations = []
        for citation in citations:
            formatted_citations.append({
                "url": citation.url,
                "chunk_id": citation.chunk_id,
                "similarity_score": citation.similarity_score,
                "text_preview": citation.text_preview
            })

        logger.info(f"Formatted {len(formatted_citations)} citations for response")
        return formatted_citations

    def enhance_citation_formatting(self, citations: List[Citation]) -> List[Citation]:
        """
        Enhance citation formatting with additional information
        """
        enhanced_citations = []
        for citation in citations:
            # Retrieve full chunk information to enhance the citation
            chunk = self.metadata_db_service.get_document_chunk(citation.chunk_id)
            if chunk:
                # Create enhanced citation with better formatting
                enhanced_citation = Citation(
                    url=chunk.get("url", citation.url),
                    chunk_id=citation.chunk_id,
                    similarity_score=citation.similarity_score,
                    text_preview=chunk.get("content", citation.text_preview)[:200] + "..."
                        if len(chunk.get("content", citation.text_preview)) > 200
                        else chunk.get("content", citation.text_preview)
                )

                # Add additional metadata if available
                if chunk.get("metadata"):
                    # Format the citation with additional context like section, page, etc.
                    metadata = chunk["metadata"]
                    section = metadata.get("section", "")
                    title = metadata.get("title", "")

                    # Enhance the text preview with context
                    if section or title:
                        context_prefix = f"[{title} - {section}] " if title and section else f"[{title}] " if title else f"[{section}] " if section else ""
                        enhanced_citation.text_preview = context_prefix + enhanced_citation.text_preview

                enhanced_citations.append(enhanced_citation)
            else:
                # If we can't get enhanced info, use the original
                enhanced_citations.append(citation)

        logger.info(f"Enhanced formatting for {len(enhanced_citations)} citations")
        return enhanced_citations

    def add_confidence_scoring(self, citations: List[Citation]) -> List[Citation]:
        """
        Add confidence scoring to citations based on similarity scores and other factors
        """
        scored_citations = []
        for citation in citations:
            # Calculate a more sophisticated confidence score
            # For now, using the similarity score directly, but this could be enhanced
            confidence_score = citation.similarity_score if citation.similarity_score is not None else 0.5
            citation.similarity_score = confidence_score  # Update the citation with the calculated score
            scored_citations.append(citation)

        logger.info(f"Added confidence scoring to {len(scored_citations)} citations")
        return scored_citations