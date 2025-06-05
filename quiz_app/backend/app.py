from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.quiz_api import router as quiz_router
from config.config import Config

# Create FastAPI app
app = FastAPI(
    title="Quiz Test API",
    description="A comprehensive quiz application backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quiz_router)

@app.get("/", summary="Root endpoint")
async def root():
    """Root endpoint providing API information"""
    return {
        "message": "Welcome to Quiz Test API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "api_endpoints": {
            "quiz_info": "/api/quiz/",
            "questions": "/api/quiz/questions",
            "categories": "/api/quiz/categories",
            "difficulties": "/api/quiz/difficulties",
            "create_session": "/api/quiz/session/create",
            "quiz_stats": "/api/quiz/stats"
        }
    }

@app.get("/health", summary="Health check")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Quiz API is running properly"}

# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint not found", "message": "The requested resource was not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    print("Starting Quiz Test API...")
    print(f"API Documentation: http://{Config.API_HOST}:{Config.API_PORT}/docs")
    print(f"ReDoc Documentation: http://{Config.API_HOST}:{Config.API_PORT}/redoc")
    
    uvicorn.run(
        "app:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=Config.DEBUG,
        log_level="info"
    )