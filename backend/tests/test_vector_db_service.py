import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.services.vector_db import VectorDBService


class TestVectorDBService:
    """Test cases for the VectorDBService"""

    @pytest.fixture
    def vector_db_service(self):
        """Create a mock vector database service for testing"""
        with patch('backend.services.vector_db.QdrantClient') as mock_qdrant:
            # Mock the Qdrant client
            mock_client = Mock()
            mock_qdrant.return_value = mock_client

            # Create the service
            service = VectorDBService()
            service.client = mock_client  # Override with mock

            return service, mock_client

    def test_store_embeddings(self, vector_db_service):
        """Test storing embeddings in Qdrant"""
        service, mock_client = vector_db_service

        # Test the method
        result = service.store_embeddings(
            doc_id="test_doc",
            chunk_id="test_chunk",
            content="test content",
            embedding=[0.1, 0.2, 0.3],
            metadata={"source": "test"}
        )

        # Assertions
        assert result is True
        mock_client.upsert.assert_called_once()
        call_args = mock_client.upsert.call_args
        assert call_args[1]['collection_name'] == service.collection_name

    def test_search_similar(self, vector_db_service):
        """Test searching for similar content"""
        service, mock_client = vector_db_service

        # Mock search results
        mock_result = [
            Mock(),
            Mock()
        ]
        mock_result[0].id = "chunk1"
        mock_result[0].payload = {
            "content": "content1",
            "source_url": "url1",
            "metadata": {"key": "value1"}
        }
        mock_result[0].score = 0.9
        mock_result[1].id = "chunk2"
        mock_result[1].payload = {
            "content": "content2",
            "source_url": "url2",
            "metadata": {"key": "value2"}
        }
        mock_result[1].score = 0.8

        mock_client.search.return_value = mock_result

        # Test the method
        result = service.search_similar([0.1, 0.2, 0.3], top_k=2)

        # Assertions
        assert len(result) == 2
        assert result[0]["chunk_id"] == "chunk1"
        assert result[0]["content"] == "content1"
        assert result[0]["url"] == "url1"
        assert result[0]["similarity_score"] == 0.9
        assert result[1]["chunk_id"] == "chunk2"

    def test_search_similar_with_selected_text(self, vector_db_service):
        """Test searching with selected text (should return empty results)"""
        service, mock_client = vector_db_service

        # Test the method with selected text
        result = service.search_similar([0.1, 0.2, 0.3], top_k=5, selected_text="selected text")

        # Assertions
        assert result == []  # Should return empty when selected_text is provided
        mock_client.search.assert_not_called()  # Should not call search method

    def test_delete_document(self, vector_db_service):
        """Test deleting a document"""
        service, mock_client = vector_db_service

        # Mock scroll results for finding chunks
        mock_scroll_result = ([Mock(), Mock()], None)  # (records, next_page_offset)
        mock_scroll_result[0][0].id = "chunk1"
        mock_scroll_result[0][1].id = "chunk2"
        mock_client.scroll.return_value = mock_scroll_result

        # Test the method
        service.delete_document("test_doc")

        # Assertions
        mock_client.scroll.assert_called_once()
        mock_client.delete.assert_called_once()