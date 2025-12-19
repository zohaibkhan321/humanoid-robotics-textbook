import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from backend.main import app
from backend.services.agent import AgentService
from backend.services.embedding import EmbeddingService
from backend.services.vector_db import VectorDBService
from backend.services.metadata_db import MetadataDBService

client = TestClient(app)


class TestIntegration:
    """Integration tests for end-to-end workflows"""

    def test_full_qa_workflow(self):
        """Test the full question-answering workflow"""
        # Mock all the services to avoid external dependencies
        with patch('backend.api.v1.answer.agent_service') as mock_agent:
            # Mock the agent service response
            mock_agent.process_query = MagicMock(return_value={
                "answer": "This is a test answer based on the context.",
                "citations": [
                    {
                        "url": "https://example.com/chapter1",
                        "chunk_id": "doc1_chunk_0",
                        "similarity_score": 0.85,
                        "text_preview": "This is a sample text preview..."
                    }
                ],
                "confidence_score": 0.9
            })

            response = client.post(
                "/api/v1/answer",
                json={
                    "query_text": "What is humanoid robotics?",
                    "selected_text": None
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "citations" in data
            assert "confidence_score" in data
            assert len(data["citations"]) > 0

    def test_embed_and_search_workflow(self):
        """Test the embed and search workflow"""
        # Mock the embedding service
        with patch('backend.api.v1.embed.text_splitter') as mock_splitter, \
             patch('backend.api.v1.embed.embedding_service') as mock_embedding, \
             patch('backend.api.v1.embed.vector_db_service') as mock_vector_db, \
             patch('backend.api.v1.embed.metadata_db_service') as mock_metadata_db:

            # Mock the text splitter
            mock_splitter.split_text.return_value = [
                {
                    'doc_id': 'test_doc',
                    'chunk_id': 'test_doc_chunk_0',
                    'content': 'Test content for humanoid robotics',
                    'source_url': 'https://example.com/test',
                    'metadata': {}
                }
            ]

            # Mock the embedding service
            mock_embedding.generate_single_embedding.return_value = [0.1, 0.2, 0.3]

            # First, test the embed endpoint
            embed_response = client.post(
                "/api/v1/embed",
                json={
                    "doc_id": "test_doc",
                    "text": "Test content for humanoid robotics",
                    "url": "https://example.com/test",
                    "metadata": {"title": "Test Document"}
                }
            )

            assert embed_response.status_code == 200
            embed_data = embed_response.json()
            assert embed_data["status"] == "success"
            assert embed_data["doc_id"] == "test_doc"
            assert embed_data["chunks_processed"] == 1

    def test_selected_text_workflow(self):
        """Test the selected text workflow"""
        # Mock the agent service to return a response for selected text
        with patch('backend.api.v1.answer.agent_service') as mock_agent:
            mock_agent.process_query = MagicMock(return_value={
                "answer": "Based on the selected text, humanoid robotics involves...",
                "citations": [],
                "confidence_score": 0.8
            })

            response = client.post(
                "/api/v1/answer",
                json={
                    "query_text": "What does this text say about stability?",
                    "selected_text": "Humanoid robots achieve stability through feedback control systems."
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "selected text" in data["answer"].lower()  # Should be based on selected text

    def test_insufficient_context_workflow(self):
        """Test the insufficient context workflow"""
        # Mock the agent service to return insufficient context
        with patch('backend.api.v1.answer.agent_service') as mock_agent:
            mock_agent.process_query = MagicMock(return_value={
                "status": "insufficient_context",
                "message": "No relevant context found to answer the question.",
                "selected_text_provided": False,
                "answer": "I couldn't find any relevant information to answer your question.",
                "citations": [],
                "confidence_score": 0.0
            })

            response = client.post(
                "/api/v1/answer",
                json={
                    "query_text": "What is the meaning of life according to the textbook?",
                    "selected_text": None
                }
            )

            # This should return a successful response, but with insufficient context info
            assert response.status_code == 200
            data = response.json()
            # The actual response structure depends on how the endpoint handles this case
            # It should return the result as is, which would then be handled by the endpoint logic

    def test_search_endpoint(self):
        """Test the search endpoint"""
        with patch('backend.api.v1.search.embedding_service') as mock_embedding, \
             patch('backend.api.v1.search.vector_db_service') as mock_vector_db:

            # Mock the embedding service
            mock_embedding.generate_query_embedding.return_value = [0.1, 0.2, 0.3]

            # Mock the vector DB service
            mock_vector_db.search_chunks.return_value = [
                {
                    "chunk_id": "test_chunk_1",
                    "content": "Test content for humanoid robotics",
                    "url": "https://example.com/test",
                    "similarity_score": 0.85,
                    "metadata": {}
                }
            ]

            response = client.post(
                "/api/v1/search",
                json={
                    "query": "humanoid robotics",
                    "top_k": 5
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "results" in data
            assert len(data["results"]) > 0
            assert data["results"][0]["chunk_id"] == "test_chunk_1"