import os
from dotenv import load_dotenv

load_dotenv()

# Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model
MODEL_NAME = "llama-3.3-70b-versatile"

# Paths
UPLOADS_PATH = "data/uploads"
VECTORSTORE_PATH = "data/vectorstores"
OUTPUTS_PATH = "outputs"
SUMMARIES_PATH = "outputs/summaries"

# RAG Settings
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
RETRIEVAL_K = 6

# Study Settings
DEFAULT_DAILY_HOURS = 3
