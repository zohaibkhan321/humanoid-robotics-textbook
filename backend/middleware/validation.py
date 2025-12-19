from fastapi import Request, HTTPException
from typing import Optional
import html
import re
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


def sanitize_input(text: str) -> str:
    """
    Sanitize input text by removing potentially dangerous content
    """
    if not text:
        return text

    # Remove potentially dangerous characters/sequences
    # HTML escape to prevent XSS
    sanitized = html.escape(text)

    # Remove or flag potential SQL injection patterns
    sql_patterns = [
        r"(?i)(union\s+select)",
        r"(?i)(drop\s+\w+)",
        r"(?i)(delete\s+from)",
        r"(?i)(insert\s+into)",
        r"(?i)(update\s+\w+\s+set)",
        r"(?i)(exec\s*\()",
        r"(?i)(execute\s*\()",
        r"(?i)(sp_\w+)",
        r"(?i)(xp_\w+)",
    ]

    for pattern in sql_patterns:
        if re.search(pattern, sanitized):
            logger.warning(f"Potential SQL injection pattern detected: {sanitized[:100]}...")
            raise HTTPException(status_code=400, detail="Invalid input detected")

    return sanitized


def validate_and_sanitize_request(request: Request, data: dict) -> dict:
    """
    Validate and sanitize request data
    """
    sanitized_data = {}

    for key, value in data.items():
        if isinstance(value, str):
            # Sanitize string values
            sanitized_value = sanitize_input(value)
            sanitized_data[key] = sanitized_value
        elif isinstance(value, dict):
            # Recursively sanitize nested dictionaries
            sanitized_data[key] = validate_and_sanitize_request(request, value)
        elif isinstance(value, list):
            # Sanitize list items if they are strings
            sanitized_list = []
            for item in value:
                if isinstance(item, str):
                    sanitized_list.append(sanitize_input(item))
                elif isinstance(item, dict):
                    sanitized_list.append(validate_and_sanitize_request(request, item))
                else:
                    sanitized_list.append(item)
            sanitized_data[key] = sanitized_list
        else:
            # Keep other types as is
            sanitized_data[key] = value

    return sanitized_data


def validate_content_length(text: Optional[str], max_length: int, field_name: str):
    """
    Validate content length against maximum allowed
    """
    if text and len(text) > max_length:
        raise HTTPException(
            status_code=422,
            detail=f"{field_name} exceeds maximum length of {max_length} characters"
        )