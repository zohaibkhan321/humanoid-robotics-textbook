import cohere
from typing import Dict, Any, List, Optional
import logging
from config.settings import settings
from services.embedding import EmbeddingService
from services.vector_db import VectorDBService
from services.metadata_db import MetadataDBService
from services.citation_service import CitationService
from models.citation import Citation

logger = logging.getLogger(__name__)


class AgentService:
    """
    Service for Cohere Agent orchestration
    Handles query processing, context retrieval, and answer generation with citations
    """

    def __init__(self):
        # Initialize Cohere client
        self.client = cohere.Client(settings.cohere_api_key)

        # Initialize other services
        self.embedding_service = EmbeddingService()
        self.vector_db_service = VectorDBService()
        self.metadata_db_service = MetadataDBService()
        self.citation_service = CitationService()

        self.model = settings.generation_model

    async def process_query(
        self,
        query_text: str,
        selected_text: Optional[str] = None,
        user_context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a user query and return an answer with citations
        """
        try:
            logger.info(f"Processing query: {query_text[:50]}...")

            # Determine context based on whether selected_text is provided
            if selected_text:
                # Selected-text-only mode: only use the provided selected text as context
                context_chunks = [{
                    "content": selected_text,
                    "url": "selected_text",
                    "chunk_id": "selected_text_chunk",
                    "similarity_score": 1.0
                }]
                logger.info("Using selected text as context")
            else:
                # Regular mode: search for relevant context
                query_embedding = self.embedding_service.generate_query_embedding(query_text)

                # Search for similar content in vector database
                search_results = self.vector_db_service.search_chunks(
                    query_embedding=query_embedding,
                    top_k=settings.default_top_k
                )

                context_chunks = search_results
                logger.info(f"Found {len(context_chunks)} context chunks from vector search")

            # If no context is available and we're in selected-text-only mode, return insufficient context
            if selected_text and len(selected_text.strip()) == 0:
                return {
                    "status": "insufficient_context",
                    "message": "Selected text is empty, cannot generate answer.",
                    "selected_text_provided": True,
                    "answer": "The selected text is empty, so I cannot provide an answer based on it.",
                    "citations": [],
                    "confidence_score": 0.0
                }

            # If no context is available in regular mode, return insufficient context
            if not context_chunks:
                return {
                    "status": "insufficient_context",
                    "message": "No relevant context found to answer the question.",
                    "selected_text_provided": bool(selected_text),
                    "answer": "I couldn't find any relevant information to answer your question.",
                    "citations": [],
                    "confidence_score": 0.0
                }

            # Prepare context for the LLM
            context_str = "\n\n".join([chunk["content"] for chunk in context_chunks])

            # Create citations from the context chunks
            raw_citations = []
            for chunk in context_chunks:
                if chunk["url"] != "selected_text":  # Don't create citations for selected text
                    citation = Citation(
                        url=chunk["url"],
                        chunk_id=chunk["chunk_id"],
                        similarity_score=chunk["similarity_score"],
                        text_preview=chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"]
                    )
                    raw_citations.append(citation)

            # Use citation service to enhance and validate citations
            validated_citations = self.citation_service.validate_citations(raw_citations)
            enhanced_citations = self.citation_service.enhance_citation_formatting(validated_citations)
            scored_citations = self.citation_service.add_confidence_scoring(enhanced_citations)

            citations = scored_citations

            # Prepare the system message based on whether we're in selected-text-only mode
            if selected_text:
                # In selected-text-only mode, be explicit about the constraint
                system_message = (
                    "You are an expert assistant for a humanoid robotics textbook. "
                    "Answer the user's question based ONLY on the provided selected text. "
                    "Do not use any external knowledge or make assumptions beyond what's in the selected text. "
                    "If the answer cannot be found in the selected text, clearly state that it's not available in the provided text. "
                    "Be accurate, concise, and cite your sources."
                )
            else:
                # Regular mode
                system_message = (
                    "You are an expert assistant for a humanoid robotics textbook. "
                    "Answer the user's question based on the provided context. "
                    "Be accurate, concise, and cite your sources. "
                    "If the answer cannot be found in the context, clearly state that."
                )

            # Format the prompt for Cohere generation
            prompt = f"{system_message}\n\nContext: {context_str}\n\nQuestion: {query_text}\n\nPlease provide a detailed answer with citations to the source material."

            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                max_tokens=1000,
                temperature=0.3,
                stop_sequences=["\n\n"]
            )

            answer = response.generations[0].text

            # Calculate a basic confidence score based on response length and context availability
            confidence_score = min(0.9, len(answer) / (len(answer) + 10))  # Simple heuristic

            result = {
                "answer": answer,
                "citations": [citation.model_dump() for citation in citations],
                "confidence_score": confidence_score
            }

            logger.info("Query processed successfully")
            return result

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise