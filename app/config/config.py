"""
Configuration settings for the PetroRAG application
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")

# Application settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
PORT = int(os.getenv("PORT", 5000))
HOST = os.getenv("HOST", "127.0.0.1")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

# Data processing settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 10))  # Number of sentences per chunk
MAX_CONTEXT_SECTIONS = int(os.getenv("MAX_CONTEXT_SECTIONS", 5))  # Number of sections to include in context

# Chat memory settings
MAX_HISTORY = int(os.getenv("MAX_HISTORY", 10))  # Maximum number of exchanges to keep in history
MEMORY_MAX_TOKENS = int(os.getenv("MEMORY_MAX_TOKENS", 1000))  # Maximum tokens to use for memory context
USE_MEMORY = False  # Disable memory functionality

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
EMBEDDINGS_FILE = os.path.join(DATA_DIR, "embeddings.pkl") 