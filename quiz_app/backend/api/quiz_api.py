from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from services.quiz_service import QuizService
from models.question_model import Question, QuizSession, QuizSummary

router = APIRouter(prefix="/api/quiz", tags=["quiz"])
quiz_service = QuizService()

@router.get("/", summary="Get API information")
async def get_api_info():
    """Get basic API information"""
    return {
        "message": "Quiz API is running",
        "version": "1.0.0",
        "total_questions": len(quiz_service.questions),
        "categories": quiz_service.get_categories(),
        "difficulties": quiz_service.get_difficulties()
    }

@router.get("/questions", response_model=List[Question], summary="Get all questions")
async def get_questions(
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty")
):
    """Get all questions, optionally filtered by category and/or difficulty"""
    try:
        if category and difficulty:
            # Filter by both category and difficulty
            questions = [q for q in quiz_service.questions 
                        if q.category.lower() == category.lower() and 
                           q.difficulty.lower() == difficulty.lower()]
        elif category:
            questions = quiz_service.get_questions_by_category(category)
        elif difficulty:
            questions = quiz_service.get_questions_by_difficulty(difficulty)
        else:
            questions = quiz_service.get_all_questions()
        
        return questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/questions/{question_id}", response_model=Question, summary="Get question by ID")
async def get_question(question_id: int):
    """Get a specific question by ID"""
    question = quiz_service.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.get("/categories", response_model=List[str], summary="Get all categories")
async def get_categories():
    """Get all available question categories"""
    return quiz_service.get_categories()

@router.get("/difficulties", response_model=List[str], summary="Get all difficulty levels")
async def get_difficulties():
    """Get all available difficulty levels"""
    return quiz_service.get_difficulties()

@router.post("/session/create", response_model=QuizSession, summary="Create new quiz session")
async def create_quiz_session(
    num_questions: int = Query(5, ge=1, le=20, description="Number of questions (1-20)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty")
):
    """Create a new quiz session with specified parameters"""
    try:
        session = quiz_service.create_quiz_session(
            num_questions=num_questions,
            category=category,
            difficulty=difficulty
        )
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}", response_model=QuizSession, summary="Get quiz session")
async def get_quiz_session(session_id: str):
    """Get an active quiz session by ID"""
    session = quiz_service.get_quiz_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Quiz session not found")
    return session

@router.post("/session/{session_id}/answer", summary="Submit answer")
async def submit_answer(
    session_id: str,
    question_id: int,
    selected_answer: int
):
    """Submit an answer for a question in a quiz session"""
    try:
        # Validate selected_answer range (0-3 for 4 options)
        if selected_answer < 0 or selected_answer > 3:
            raise HTTPException(status_code=400, detail="Selected answer must be between 0 and 3")
        
        success = quiz_service.submit_answer(session_id, question_id, selected_answer)
        if success:
            return {"message": "Answer submitted successfully", "question_id": question_id, "selected_answer": selected_answer}
        else:
            raise HTTPException(status_code=400, detail="Failed to submit answer")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/{session_id}/complete", response_model=QuizSummary, summary="Complete quiz")
async def complete_quiz(session_id: str):
    """Complete a quiz session and get results"""
    try:
        summary = quiz_service.complete_quiz(session_id)
        return summary
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}", summary="Delete quiz session")
async def delete_quiz_session(session_id: str):
    """Delete an active quiz session"""
    if session_id in quiz_service.active_sessions:
        del quiz_service.active_sessions[session_id]
        return {"message": "Quiz session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Quiz session not found")

@router.get("/stats", summary="Get quiz statistics")
async def get_quiz_stats():
    """Get overall quiz statistics"""
    categories = quiz_service.get_categories()
    difficulties = quiz_service.get_difficulties()
    
    stats = {
        "total_questions": len(quiz_service.questions),
        "total_categories": len(categories),
        "total_difficulties": len(difficulties),
        "active_sessions": len(quiz_service.active_sessions),
        "categories": categories,
        "difficulties": difficulties,
        "questions_by_category": {cat: len(quiz_service.get_questions_by_category(cat)) for cat in categories},
        "questions_by_difficulty": {diff: len(quiz_service.get_questions_by_difficulty(diff)) for diff in difficulties}
    }
    
    return stats

@router.post("/cleanup", summary="Cleanup expired sessions")
async def cleanup_sessions():
    """Manually trigger cleanup of expired sessions"""
    try:
        cleaned_count = quiz_service.cleanup_expired_sessions()
        return {"message": f"Cleaned up {cleaned_count} expired sessions"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))