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

# ✅ FIXED: Serve frontend static files in production
if settings.is_production:
    # Go up TWO levels: from backend/app/ to project root, then to frontend
    current_file = Path(__file__).resolve()  # backend/app/main.py
    project_root = current_file.parent.parent.parent  # Go up 3 levels to project root
    frontend_path = project_root / "frontend"
    
    print(f"🔍 Looking for frontend at: {frontend_path}")
    print(f"📁 Frontend exists: {frontend_path.exists()}")
    
    if frontend_path.exists():
        app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
        print("✅ Frontend mounted successfully!")
    else:
        print("❌ Frontend folder not found!")

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
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent
        frontend_path = project_root / "frontend"
        print(f"📁 Looking for frontend at: {frontend_path}")
        print(f"📁 Frontend exists: {frontend_path.exists()}")
        if frontend_path.exists():
            print(f"📁 Frontend contents: {list(frontend_path.glob('*'))}")
    
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