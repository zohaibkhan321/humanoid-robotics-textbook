#!/usr/bin/env python3
"""
Test script to check Qdrant connection
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from config.settings import settings
from qdrant_client import QdrantClient

print("Testing Qdrant connection...")

print(f"QDRANT_URL: {settings.qdrant_url}")
print(f"QDRANT_API_KEY: {'***' if settings.qdrant_api_key else 'None'}")

try:
    print("Creating Qdrant client...")
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        prefer_grpc=True
    )
    print("Qdrant client created successfully!")

    print("Testing connection by listing collections...")
    collections = client.get_collections()
    print(f"Available collections: {collections}")
    print("Qdrant connection test successful!")

except Exception as e:
    print(f"Qdrant connection failed: {e}")
    import traceback
    traceback.print_exc()