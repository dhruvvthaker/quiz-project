from typing import List, Optional
from pydantic import BaseModel

class Question(BaseModel):
    id: int
    question: str
    options: List[str]
    correct_answer: int
    category: str
    difficulty: str

class QuizResponse(BaseModel):
    question_id: int
    selected_answer: int

class QuizResult(BaseModel):
    question_id: int
    question: str
    options: List[str]
    selected_answer: int
    correct_answer: int
    is_correct: bool
    category: str
    difficulty: str

class QuizSummary(BaseModel):
    total_questions: int
    correct_answers: int
    wrong_answers: int
    score_percentage: float
    results: List[QuizResult]

class QuizSession(BaseModel):
    session_id: str
    questions: List[Question]
    responses: List[QuizResponse] = []
    is_completed: bool = False
    created_at: Optional[str] = None