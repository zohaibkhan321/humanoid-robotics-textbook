import time
from typing import Dict
from fastapi import HTTPException
from collections import defaultdict
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple in-memory rate limiter middleware
    Tracks requests by IP address and enforces rate limits
    """

    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.limit = settings.rate_limit_requests
        self.window = settings.rate_limit_window  # in seconds

    def is_allowed(self, client_ip: str) -> bool:
        """
        Check if a request from the given IP is allowed
        """
        current_time = time.time()

        # Clean old requests outside the time window
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < self.window
        ]

        # Check if we're under the limit
        if len(self.requests[client_ip]) < self.limit:
            # Add current request
            self.requests[client_ip].append(current_time)
            return True

        # Check if oldest request is outside the window
        # If so, we can allow the request by removing the oldest
        oldest_request = self.requests[client_ip][0]
        if current_time - oldest_request >= self.window:
            self.requests[client_ip].pop(0)  # Remove oldest
            self.requests[client_ip].append(current_time)  # Add current
            return True

        # Rate limit exceeded
        return False


# Global rate limiter instance
rate_limiter = RateLimiter()


def check_rate_limit(client_ip: str) -> None:
    """
    Check rate limit and raise HTTPException if exceeded
    """
    if not rate_limiter.is_allowed(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {settings.rate_limit_requests} requests per {settings.rate_limit_window} seconds."
        )