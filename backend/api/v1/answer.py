from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging
from models.query import Query as QueryModel
from services.agent import AgentService
from config.settings import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
agent_service = AgentService()


@router.post("/answer")
async def get_answer(request: QueryModel) -> Dict[str, Any]:
    """
    Generate answer to user question with citations
    POST /api/v1/answer
    """
    try:
        logger.info(f"Processing answer request for query: {request.query_text[:50]}...")

        # Validate query length
        if len(request.query_text) > settings.max_query_length:
            raise HTTPException(status_code=400, detail=f"Query exceeds maximum length of {settings.max_query_length} characters")

        # If selected_text is provided, validate its length
        if request.selected_text and len(request.selected_text) > settings.max_selected_text_length:
            raise HTTPException(status_code=400, detail=f"Selected text exceeds maximum length of {settings.max_selected_text_length} characters")

        # Use the agent service to generate the answer
        result = await agent_service.process_query(
            query_text=request.query_text,
            selected_text=request.selected_text,
            user_context=request.user_context,
            session_id=request.session_id
        )

        # Check if the result indicates insufficient context
        if result.get("status") == "insufficient_context":
            # Return a 412 Precondition Failed response for insufficient selected text
            if result.get("selected_text_provided"):
                return {
                    "status": "insufficient_context",
                    "message": result.get("message", "Insufficient context in selected text to answer the question."),
                    "selected_text_provided": True
                }
            else:
                raise HTTPException(
                    status_code=404,
                    detail=result.get("message", "No relevant context found to answer the question.")
                )

        # Return the response with proper structure for successful answers
        response = {
            "query": request.query_text,
            "answer": result.get("answer", ""),
            "citations": result.get("citations", []),
            "confidence_score": result.get("confidence_score", 0.0)
        }

        logger.info("Answer generated successfully")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing answer request: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")