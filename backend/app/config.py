import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    
    # API Endpoints
    WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
    ARXIV_API = "http://export.arxiv.org/api/query"
    NEWS_API = "https://newsapi.org/v2/everything"
    
    # OpenAI Settings
    OPENAI_MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 1500
    TEMPERATURE = 0.7
    
    # App Settings
    MAX_SOURCES = 5
    REQUEST_TIMEOUT = 30
    CACHE_TTL = 3600  # 1 hour
    
    # Rate Limiting
    REQUESTS_PER_MINUTE = 10
    
    @property
    def is_production(self):
        return os.getenv("ENVIRONMENT", "development") == "production"

settings = Settings()