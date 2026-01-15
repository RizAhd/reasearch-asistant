from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import asyncio
from ..schemas.request import ResearchRequest, ResearchDepth
from ..schemas.response import ResearchResponse, HealthResponse
from ..services.research_service import research_service
from ..config import settings
import time

router = APIRouter(prefix="/api/v1", tags=["research"])

# Store active requests for rate limiting (simple in-memory solution)
active_requests = {}
REQUEST_LIMIT = 5  # Max concurrent requests per IP

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        uptime=time.time() - startup_time,
        api_keys={
            "openai": bool(settings.OPENAI_API_KEY),
            "newsapi": bool(settings.NEWS_API_KEY)
        }
    )

@router.post("/research", response_model=ResearchResponse)
async def research_endpoint(
    request: ResearchRequest,
    background_tasks: BackgroundTasks
):
    """
    Main research endpoint.
    
    - **query**: Your research question
    - **depth**: quick, balanced, or deep
    - **include_sources**: Which sources to use
    - **max_sources**: Maximum number of sources to return
    """
    
    # Simple rate limiting by IP (for demo)
    client_ip = "demo"  # In production, get from request.client.host
    
    if client_ip in active_requests:
        if active_requests[client_ip] >= REQUEST_LIMIT:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again in a moment."
            )
        active_requests[client_ip] += 1
    else:
        active_requests[client_ip] = 1
    
    try:
        # Adjust parameters based on depth
        if request.depth == ResearchDepth.QUICK:
            max_sources = 3
            include_sources = ["wikipedia"]
        elif request.depth == ResearchDepth.DEEP:
            max_sources = 8
        else:  # balanced
            max_sources = request.max_sources or 5
        
        # Perform research
        result = await research_service.research(
            query=request.query,
            include_sources=request.include_sources,
            max_sources=max_sources
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {str(e)}"
        )
    finally:
        # Clean up rate limiting
        if client_ip in active_requests:
            active_requests[client_ip] -= 1
            if active_requests[client_ip] <= 0:
                del active_requests[client_ip]

@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify the API is working"""
    return {
        "message": "Research Assistant API is running!",
        "endpoints": {
            "POST /api/v1/research": "Main research endpoint",
            "GET /api/v1/health": "Health check",
            "GET /docs": "API documentation"
        },
        "available_sources": ["wikipedia", "arxiv", "news"]
    }

# Store startup time for uptime calculation
startup_time = time.time()