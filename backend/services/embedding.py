import cohere
from typing import List
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating embeddings using Cohere API
    """
    def __init__(self):
        try:
            self.client = cohere.Client(settings.cohere_api_key)
            self.model = settings.embedding_model
            logger.info("Embedding service initialized with Cohere client")
        except Exception as e:
            logger.error(f"Error initializing Cohere client: {e}")
            raise

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts
        """
        try:
            logger.info(f"Generating embeddings for {len(texts)} texts")
            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type=settings.embedding_input_type  # Using configurable input type
            )

            embeddings = [embedding for embedding in response.embeddings]
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a query (using search_query input type)
        """
        try:
            logger.info(f"Generating query embedding for: {query[:50]}...")
            response = self.client.embed(
                texts=[query],
                model=self.model,
                input_type="search_query"
            )

            embedding = response.embeddings[0]
            logger.info("Successfully generated query embedding")
            return embedding
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            raise

    def generate_single_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        """
        try:
            logger.info(f"Generating single embedding for text of length {len(text)}")
            response = self.client.embed(
                texts=[text],
                model=self.model,
                input_type=settings.embedding_input_type
            )

            embedding = response.embeddings[0]
            logger.info("Successfully generated single embedding")
            return embedding
        except Exception as e:
            logger.error(f"Error generating single embedding: {e}")
            raise