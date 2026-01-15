# backend/app/schemas/response.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class Source(BaseModel):
    title: str
    content: str
    url: str
    source_type: str
    confidence: float = 0.0
    metadata: Optional[Dict[str, Any]] = None

class ResearchResponse(BaseModel):
    answer: str
    sources: List[Source]
    query: str
    tokens_used: int
    processing_time: float
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Artificial intelligence (AI) is...",
                "sources": [
                    {
                        "title": "Artificial intelligence",
                        "content": "AI is the simulation...",
                        "url": "https://en.wikipedia.org/wiki/AI",
                        "source_type": "wikipedia"
                    }
                ],
                "query": "What is artificial intelligence?",
                "tokens_used": 450,
                "processing_time": 2.5,
                "timestamp": "2024-01-15T10:30:00"
            }
        }

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime: float
    api_keys: Dict[str, bool]