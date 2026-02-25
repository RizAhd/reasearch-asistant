from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes import research
import os
from pathlib import Path
from .config import settings

app = FastAPI(
    title="Universal Research Assistant API",
    description="AI-powered research assistant that combines Wikipedia and NewsAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS based on environment
if settings.is_production:
    allowed_origins = [
        "https://reasearch-asistant.onrender.com",  # Your actual domain
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

# ✅ CRITICAL FIX: Include API routes FIRST before static files
app.include_router(research.router)

# ✅ Then serve frontend static files in production (with prefix to avoid conflicts)
if settings.is_production:
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent
    frontend_path = project_root / "frontend"
    
    print(f"🔍 Looking for frontend at: {frontend_path}")
    print(f"📁 Frontend exists: {frontend_path.exists()}")
    
    if frontend_path.exists():
        # Mount static files but exclude API routes
        app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
        print("✅ Frontend mounted successfully!")
    else:
        print("❌ Frontend folder not found!")

@app.get("/api/health")
async def api_health_check():
    """Simple API health check endpoint (without /api/v1 prefix)"""
    return {
        "status": "healthy",
        "environment": "production" if settings.is_production else "development",
        "api_keys": {
            "openai": bool(settings.OPENAI_API_KEY),
            "newsapi": bool(settings.NEWS_API_KEY)
        }
    }

@app.get("/debug/routes")
async def debug_routes():
    """List all registered routes for debugging"""
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "name": route.name,
            "methods": list(route.methods) if hasattr(route, "methods") else None
        })
    return {"routes": routes, "total": len(routes)}

@app.on_event("startup")
async def startup_event():
    """Runs on app startup"""
    print("🚀 Research Assistant API starting...")
    print(f"📊 Environment: {'Production' if settings.is_production else 'Development'}")
    print(f"🔑 OpenAI configured: {bool(settings.OPENAI_API_KEY)}")
    print(f"📰 NewsAPI configured: {bool(settings.NEWS_API_KEY)}")
    print(f"📝 Total routes registered: {len(app.routes)}")
    
    if settings.is_production:
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent
        frontend_path = project_root / "frontend"
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