import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    
    # API Endpoints
    WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
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
        """Check if running in production environment"""
        return os.getenv("ENVIRONMENT", "development").lower() == "production"
    
    @property
    def api_keys_configured(self):
        """Check if required API keys are configured"""
        return {
            "openai": bool(self.OPENAI_API_KEY),
            "newsapi": bool(self.NEWS_API_KEY)
        }

# Create global settings instance
settings = Settings()