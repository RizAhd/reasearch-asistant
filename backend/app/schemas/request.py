# backend/app/schemas/request.py
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class ResearchDepth(str, Enum):
    QUICK = "quick"
    BALANCED = "balanced"
    DEEP = "deep"

class ResearchRequest(BaseModel):
    query: str
    depth: ResearchDepth = ResearchDepth.BALANCED
    include_sources: List[str] = ["wikipedia", "arxiv", "news"]
    max_sources: int = 5
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is artificial intelligence?",
                "depth": "balanced",
                "include_sources": ["wikipedia", "arxiv", "news"],
                "max_sources": 5
            }
        }