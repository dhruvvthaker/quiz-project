import os
from pathlib import Path

class Config:
    # Base directory
    BASE_DIR = Path(__file__).parent.parent
    
    # Data file path
    QUESTIONS_FILE = BASE_DIR / "data" / "questions.json"
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Quiz Configuration
    DEFAULT_QUIZ_SIZE = 5
    MAX_QUIZ_SIZE = 20
    
    # Session Configuration
    SESSION_TIMEOUT = 3600  # 1 hour in seconds