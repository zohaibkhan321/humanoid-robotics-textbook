from typing import List, Dict, Any
from config.settings import settings
import re


class TextSplitter:
    """
    Utility class for splitting text into chunks with overlap to preserve context
    Implements the text chunking strategy specified in research.md:
    - 200-500 token chunks with overlap to preserve context across boundaries
    - Recursive splitting to handle different content types
    """

    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """
        Initialize the text splitter with configurable chunk size and overlap
        """
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

    def split_text(self, text: str, doc_id: str, source_url: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Split text into chunks with overlap to preserve context
        """
        if not text or len(text.strip()) == 0:
            return []

        if metadata is None:
            metadata = {}

        # First, roughly estimate tokens by counting words (1 token ~ 4 chars or 0.75 words)
        # For more accurate tokenization, we could use a proper tokenizer
        paragraphs = self._split_by_paragraphs(text)

        chunks = []
        chunk_id_counter = 0

        for paragraph in paragraphs:
            if len(paragraph.strip()) == 0:
                continue

            # If paragraph is smaller than chunk size, use as is
            if self._estimate_tokens(paragraph) <= self.chunk_size:
                chunk_id = f"{doc_id}_chunk_{chunk_id_counter}"
                chunks.append({
                    'doc_id': doc_id,
                    'chunk_id': chunk_id,
                    'content': paragraph.strip(),
                    'source_url': source_url,
                    'metadata': metadata
                })
                chunk_id_counter += 1
            else:
                # Split the paragraph into smaller chunks
                sub_chunks = self._split_large_paragraph(paragraph, doc_id, source_url, metadata)
                for sub_chunk in sub_chunks:
                    sub_chunk['chunk_id'] = f"{doc_id}_chunk_{chunk_id_counter}"
                    chunks.append(sub_chunk)
                    chunk_id_counter += 1

        return chunks

    def _split_by_paragraphs(self, text: str) -> List[str]:
        """
        Split text by paragraphs first to preserve semantic boundaries
        """
        # Split by double newlines first (paragraphs)
        paragraphs = re.split(r'\n\s*\n', text)
        # Clean up and filter empty paragraphs
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return paragraphs

    def _split_large_paragraph(self, text: str, doc_id: str, source_url: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split a large paragraph into smaller chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            # Determine the end position
            end = start + self.chunk_size

            # If we're near the end, include the rest
            if end >= len(text):
                end = len(text)
            else:
                # Try to find a good breaking point (sentence or word boundary)
                end = self._find_break_point(text, start, end)

            chunk_content = text[start:end].strip()

            if chunk_content:
                chunks.append({
                    'doc_id': doc_id,
                    'content': chunk_content,
                    'source_url': source_url,
                    'metadata': metadata
                })

            # Move start position with overlap
            start = end - self.chunk_overlap

            # If start >= len(text), we're done
            if start >= len(text):
                break

            # If the overlap section is too small, advance to next chunk_size
            if len(text) - start < self.chunk_overlap:
                start = len(text)

        return chunks

    def _find_break_point(self, text: str, start: int, proposed_end: int) -> int:
        """
        Find a good breaking point in the text (prefer sentence boundaries, then word boundaries)
        """
        # Look for sentence boundaries near the proposed end
        sentence_end = text.rfind('.', start, proposed_end)
        if sentence_end != -1 and sentence_end > start + 50:  # Ensure we don't cut too early
            return sentence_end + 1  # Include the period

        # Look for paragraph boundaries
        paragraph_end = text.rfind('\n\n', start, proposed_end)
        if paragraph_end != -1 and paragraph_end > start + 50:
            return paragraph_end + 2  # Include the newlines

        # Look for word boundaries
        word_end = text.rfind(' ', start, proposed_end)
        if word_end != -1 and word_end > start + 50:
            return word_end

        # If no good break point found, use the proposed end
        return proposed_end

    def _estimate_tokens(self, text: str) -> int:
        """
        Roughly estimate the number of tokens in the text
        This is a simple heuristic: 1 token ~ 0.75 words or 4 characters
        For more accurate tokenization, use a proper tokenizer like tiktoken
        """
        # Count words as a rough estimate
        words = len(text.split())
        return int(words * 1.3)  # Rough conversion factor