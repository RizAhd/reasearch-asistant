from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes import research
import os
from pathlib import Path
from .config import settings

app = FastAPI(
    title="Universal Research Assistant API",
    description="AI-powered research assistant that combines Wikipedia, arXiv, and NewsAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS based on environment
if settings.is_production:
    allowed_origins = [
        "https://research-assistant-backend.onrender.com",
        "http://localhost:3000",
        "http://localhost:8000"
    ]
else:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files in production
if settings.is_production:
    frontend_path = Path(__file__).parent.parent / "frontend"
    if frontend_path.exists():
        app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")

# Include routers
app.include_router(research.router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Universal Research Assistant API",
        "docs": "/docs",
        "health": "/api/v1/health",
        "version": "1.0.0",
        "sources": ["Wikipedia", "arXiv", "NewsAPI"],
        "environment": "production" if settings.is_production else "development"
    }

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "environment": "production" if settings.is_production else "development",
        "api_keys": {
            "openai": bool(settings.OPENAI_API_KEY),
            "newsapi": bool(settings.NEWS_API_KEY)
        }
    }

@app.on_event("startup")
async def startup_event():
    """Runs on app startup"""
    print("🚀 Research Assistant API starting...")
    print(f"📊 Environment: {'Production' if settings.is_production else 'Development'}")
    print(f"🔑 OpenAI configured: {bool(settings.OPENAI_API_KEY)}")
    print(f"📰 NewsAPI configured: {bool(settings.NEWS_API_KEY)}")
    
    if settings.is_production:
        frontend_path = Path(__file__).parent.parent / "frontend"
        print(f"📁 Frontend path: {frontend_path}")
        print(f"📁 Frontend exists: {frontend_path.exists()}")
    
    print("✅ API ready!")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=not settings.is_production
    )