import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, Any, List, Optional
from config.settings import settings
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MetadataDBService:
    """
    Service for interacting with Neon Postgres metadata storage
    """
    def __init__(self):
        self.conn_string = settings.neon_conn

    def get_connection(self):
        """
        Get a connection to the database
        """
        try:
            return psycopg2.connect(self.conn_string)
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    def initialize_tables(self):
        """
        Initialize the required tables if they don't exist
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create documents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                doc_id TEXT PRIMARY KEY,
                chunk_id TEXT UNIQUE,
                content TEXT,
                url TEXT,
                metadata JSONB,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

    def store_document_chunk(self, doc_id: str, chunk_id: str, content: str, url: str, metadata: Dict[str, Any]):
        """
        Store document chunk metadata in the database
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO documents (doc_id, chunk_id, content, url, metadata)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (chunk_id) DO UPDATE SET
                    content = EXCLUDED.content,
                    url = EXCLUDED.url,
                    metadata = EXCLUDED.metadata,
                    created_at = NOW()
            """, (doc_id, chunk_id, content, url, json.dumps(metadata)))

            conn.commit()
            cursor.close()
            conn.close()

            logger.info(f"Stored document chunk: {chunk_id}")
        except Exception as e:
            logger.error(f"Error storing document chunk {chunk_id}: {e}")
            raise

    def get_document_chunk(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document chunk by its chunk_id
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT doc_id, chunk_id, content, url, metadata, created_at
                FROM documents
                WHERE chunk_id = %s
            """, (chunk_id,))

            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                return dict(result)
            return None
        except Exception as e:
            logger.error(f"Error retrieving document chunk {chunk_id}: {e}")
            raise

    def get_document_chunks(self, doc_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all chunks for a specific document
        """
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT doc_id, chunk_id, content, url, metadata, created_at
            FROM documents
            WHERE doc_id = %s
            ORDER BY created_at
        """, (doc_id,))

        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return [dict(result) for result in results]

    def delete_document(self, doc_id: str):
        """
        Delete all chunks associated with a document
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM documents
            WHERE doc_id = %s
        """, (doc_id,))

        conn.commit()
        cursor.close()
        conn.close()

    def search_documents(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search documents by content (basic full-text search)
        """
        conn = self.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT doc_id, chunk_id, content, url, metadata, created_at
            FROM documents
            WHERE content ILIKE %s
            ORDER BY created_at DESC
            LIMIT %s
        """, (f'%{query}%', limit))

        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return [dict(result) for result in results]