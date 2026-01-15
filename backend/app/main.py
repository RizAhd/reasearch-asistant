from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes import research
import os
from .config import settings

# Create FastAPI app
app = FastAPI(
    title="Universal Research Assistant API",
    description="AI-powered research assistant that combines Wikipedia, arXiv, and NewsAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        "sources": ["Wikipedia", "arXiv", "NewsAPI"]
    }

@app.on_event("startup")
async def startup_event():
    """Runs on app startup"""
    print("🚀 Research Assistant API starting...")
    print(f"📊 Environment: {'Production' if settings.is_production else 'Development'}")
    print(f"🔑 OpenAI configured: {bool(settings.OPENAI_API_KEY)}")
    print(f"📰 NewsAPI configured: {bool(settings.NEWS_API_KEY)}")
    print("✅ API ready!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )