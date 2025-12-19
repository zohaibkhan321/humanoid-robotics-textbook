import pytest
from unittest.mock import Mock, patch
from backend.services.embedding import EmbeddingService


class TestEmbeddingService:
    """Test cases for the EmbeddingService"""

    @pytest.fixture
    def embedding_service(self):
        """Create a mock embedding service for testing"""
        with patch('backend.services.embedding.cohere') as mock_cohere:
            # Mock the Cohere client
            mock_client = Mock()
            mock_cohere.Client.return_value = mock_client

            # Create the service
            service = EmbeddingService()
            service.client = mock_client  # Override with mock

            return service, mock_client

    def test_generate_single_embedding(self, embedding_service):
        """Test generating a single embedding"""
        service, mock_client = embedding_service

        # Mock the response
        mock_response = Mock()
        mock_response.embeddings = [[0.1, 0.2, 0.3]]
        mock_client.embed.return_value = mock_response

        # Test the method
        result = service.generate_single_embedding("test text")

        # Assertions
        assert result == [0.1, 0.2, 0.3]
        mock_client.embed.assert_called_once_with(
            texts=["test text"],
            model=service.model,
            input_type="search_document"
        )

    def test_generate_query_embedding(self, embedding_service):
        """Test generating a query embedding"""
        service, mock_client = embedding_service

        # Mock the response
        mock_response = Mock()
        mock_response.embeddings = [[0.4, 0.5, 0.6]]
        mock_client.embed.return_value = mock_response

        # Test the method
        result = service.generate_query_embedding("test query")

        # Assertions
        assert result == [0.4, 0.5, 0.6]
        mock_client.embed.assert_called_once_with(
            texts=["test query"],
            model=service.model,
            input_type="search_query"
        )

    def test_generate_embeddings(self, embedding_service):
        """Test generating multiple embeddings"""
        service, mock_client = embedding_service

        # Mock the response
        mock_response = Mock()
        mock_response.embeddings = [[0.1, 0.2], [0.3, 0.4]]
        mock_client.embed.return_value = mock_response

        # Test the method
        result = service.generate_embeddings(["text1", "text2"])

        # Assertions
        assert result == [[0.1, 0.2], [0.3, 0.4]]
        mock_client.embed.assert_called_once_with(
            texts=["text1", "text2"],
            model=service.model,
            input_type="search_document"
        )