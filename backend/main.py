from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
from config.settings import settings
from services.monitoring import metrics_collector, get_metrics_for_prometheus

# Import API routers
from api.v1.embed import router as embed_router
from api.v1.search import router as search_router
from api.v1.answer import router as answer_router

# Import middleware
from middleware.rate_limit import check_rate_limit

# Configure logging
logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    # Startup
    logger.info("Starting up RAG Chatbot API")

    # Initialize services here if needed
    # For example, initialize vector DB collection, etc.

    yield

    # Shutdown
    logger.info("Shutting down RAG Chatbot API")


# Create FastAPI app
app = FastAPI(
    title="RAG Chatbot API for Humanoid Robotics Textbook",
    description="API for retrieving and answering questions about humanoid robotics textbook content",
    version="1.0.0",
    lifespan=lifespan
)

# Add security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware for additional security
if settings.debug:
    # In development, allow all hosts
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
else:
    # In production, restrict to specific hosts
    allowed_hosts = [host.replace("https://", "").replace("http://", "").split(":")[0]
                     for host in settings.cors_origins] + ["localhost", "127.0.0.1"]
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# Include API routers
app.include_router(embed_router, prefix="/api/v1", tags=["embed"])
app.include_router(search_router, prefix="/api/v1", tags=["search"])
app.include_router(answer_router, prefix="/api/v1", tags=["answer"])


# Global exception handlers
@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    logger.error(f"Internal server error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error"}
    )


@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc: Exception):
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"status": "error", "message": "Validation error", "details": str(exc)}
    )


@app.exception_handler(429)
async def rate_limit_exception_handler(request: Request, exc: Exception):
    logger.warning(f"Rate limit exceeded: {exc}")
    return JSONResponse(
        status_code=429,
        content={"status": "error", "message": "Rate limit exceeded"}
    )


@app.get("/")
def read_root():
    return {"message": "RAG Chatbot API for Humanoid Robotics Textbook"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "RAG Chatbot API is running"}


@app.get("/ready")
def readiness_check():
    """
    Readiness check for container orchestration
    """
    # Here you would check if all required services are available
    # For now, just return healthy
    return {"status": "ready", "message": "RAG Chatbot API is ready to serve requests"}


@app.get("/metrics")
def get_metrics():
    """
    Metrics endpoint for monitoring (Prometheus format)
    """
    return get_metrics_for_prometheus()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware to track request processing time and log metrics
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    # Record the request in metrics
    endpoint = f"{request.method} {request.url.path}"
    metrics_collector.record_request(
        endpoint=endpoint,
        response_time=process_time,
        is_error=response.status_code >= 400
    )

    # Add process time to response headers
    response.headers["X-Process-Time"] = str(process_time)

    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level
    )
