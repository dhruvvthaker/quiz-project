from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.quiz_api import router as quiz_router

app = FastAPI(
    title="Quiz Backend",
    description="A simple FastAPI backend to serve quiz questions",
    version="1.0.0",
)

# Configure CORS to allow any origin during development.
# In production, replace ["*"] with the actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the quiz_router under /api, so endpoints become:
#   GET /api/get-questions
#   GET /api/get-question/{id}
app.include_router(quiz_router, prefix="/api")

@app.get("/")
async def root():
    """
    Health check endpoint—use this to verify your server is running.
    """
    return {"message": "Quiz Backend is running!"}
