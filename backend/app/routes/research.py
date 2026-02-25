from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from typing import List, Optional
import asyncio
import time
from ..schemas.request import ResearchRequest, ResearchDepth
from ..schemas.response import ResearchResponse, HealthResponse
from ..services.research_service import research_service
from ..config import settings

router = APIRouter(prefix="/api/v1", tags=["research"])

# Simple rate limiting (in-memory)
active_requests = {}
REQUEST_LIMIT = 10  # Increased from 5 to 10

# Store startup time
startup_time = time.time()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint - monitors API status"""
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
    
    - **query**: Your research question (required)
    - **depth**: quick, balanced, or deep
    - **include_sources**: Which sources to use (wikipedia, news)
    - **max_sources**: Maximum number of sources to return
    """
    
    # Simple rate limiting (in production, use Redis)
    client_ip = "demo"  # In production: request.client.host
    
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
        # Validate query
        if not request.query or len(request.query.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="Query must be at least 3 characters long"
            )
        
        if len(request.query) > 500:
            raise HTTPException(
                status_code=400,
                detail="Query too long. Maximum 500 characters."
            )
        
        # Adjust parameters based on depth
        if request.depth == ResearchDepth.QUICK:
            max_sources = 3
            # For quick mode, only use Wikipedia
            include_sources = ["wikipedia"]
        elif request.depth == ResearchDepth.DEEP:
            max_sources = 8
            include_sources = request.include_sources or ["wikipedia", "news"]
        else:  # balanced
            max_sources = request.max_sources or 5
            include_sources = request.include_sources or ["wikipedia", "news"]
        
        # Filter out any arXiv references just in case
        include_sources = [s for s in include_sources if s != "arxiv"]
        
        # Perform research
        result = await research_service.research(
            query=request.query.strip(),
            include_sources=include_sources,
            max_sources=max_sources
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Research endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Research failed. Please try again."
        )
    finally:
        # Clean up rate limiting
        if client_ip in active_requests:
            active_requests[client_ip] -= 1
            if active_requests[client_ip] <= 0:
                del active_requests[client_ip]

@router.options("/research")
async def research_options():
    """Handle preflight CORS requests"""
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "3600"
        }
    )

@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify the API is working"""
    return {
        "message": "Research Assistant API is running!",
        "status": "operational",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/v1/research": "Main research endpoint",
            "GET /api/v1/health": "Health check",
            "GET /docs": "API documentation"
        },
        "available_sources": ["wikipedia", "news"],
        "environment": "production" if settings.is_production else "development"
    }

@router.get("/stats")
async def get_stats():
    """Get basic usage statistics"""
    return {
        "active_requests": len(active_requests),
        "total_requests_handled": sum(active_requests.values()),
        "uptime_seconds": time.time() - startup_time,
        "rate_limit": REQUEST_LIMIT
    }