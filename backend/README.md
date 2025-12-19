# RAG Chatbot for Humanoid Robotics Textbook

This backend service provides a Retrieval-Augmented Generation (RAG) chatbot for the humanoid robotics textbook. It allows users to ask questions about book content and receive accurate answers with proper citations.

## Features

- **Question Answering**: Ask questions about the humanoid robotics textbook content
- **Citation Support**: All answers include proper citations to source material
- **Selected Text Mode**: Ask questions constrained to specific selected text
- **Document Ingestion**: Support for ingesting new documents via URL or direct text
- **Vector Search**: Fast semantic search using Cohere embeddings and Qdrant
- **Security**: Rate limiting, input validation, and CORS protection

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Vector Database**: Qdrant
- **Metadata Storage**: Neon Postgres
- **Embeddings**: Cohere
- **Generation**: OpenAI GPT models

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create and configure your environment file:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `COHERE_API_KEY` | Your Cohere API key |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `QDRANT_URL` | Qdrant endpoint URL |
| `QDRANT_API_KEY` | Qdrant API key (if using cloud) |
| `NEON_CONN` | Neon Postgres connection string |
| `CORS_ORIGINS` | Allowed origins for CORS (JSON array) |
| `RATE_LIMIT_REQUESTS` | Max requests per time window |
| `RATE_LIMIT_WINDOW` | Time window in seconds |
| `EMBEDDING_MODEL` | Cohere embedding model name |
| `GENERATION_MODEL` | OpenAI model for generation |
| `DEBUG` | Enable debug mode |

## Running the Service

### Development
```bash
python main.py
# Or with uvicorn directly:
uvicorn main:app --reload --port 8000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### `/api/v1/embed` (POST)
Generate and store embeddings for book content.

Request body:
```json
{
  "url": "string (optional, URL to fetch content from)",
  "text": "string (optional, direct text content to embed)",
  "doc_id": "string (unique identifier for the document)",
  "metadata": "object (additional metadata about the document)"
}
```

### `/api/v1/search` (POST)
Search for relevant content based on query.

Request body:
```json
{
  "query": "string (search query)",
  "top_k": "integer (number of results to return, default: 5)",
  "selected_text": "string (optional, if provided, search is constrained to this text)"
}
```

### `/api/v1/answer` (POST)
Generate answer to user question with citations.

Request body:
```json
{
  "query": "string (user question)",
  "selected_text": "string (optional, if provided, answer only from this text)",
  "session_id": "string (optional, for conversation history)"
}
```

## Testing

Run the tests with pytest:
```bash
pytest tests/
```

## Docker

Build and run with Docker:
```bash
# Build the image
docker build -t rag-chatbot-backend .

# Run the container
docker run -p 8000:8000 --env-file .env rag-chatbot-backend
```

## Health Checks

- `/health` - Health check endpoint
- `/ready` - Readiness check endpoint

## Security Features

- Rate limiting (100 requests per minute per IP by default)
- Input validation and sanitization
- CORS protection
- SQL injection and XSS prevention
- Trusted host middleware

## Architecture

The system follows a service-oriented architecture:

- `api/` - API route definitions
- `services/` - Business logic services
- `models/` - Pydantic models for data validation
- `utils/` - Utility functions
- `config/` - Configuration and settings
- `middleware/` - Security and validation middleware

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `400` - Bad request (validation error)
- `404` - Not found
- `412` - Precondition failed (insufficient context in selected text mode)
- `422` - Unprocessable entity
- `429` - Rate limit exceeded
- `500` - Internal server error