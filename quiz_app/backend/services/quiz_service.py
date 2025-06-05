import json
import random
import uuid
from datetime import datetime
from typing import List, Optional, Dict
from models.question_model import Question, QuizSession, QuizResponse, QuizResult, QuizSummary
from config.config import Config

class QuizService:
    def __init__(self):
        self.questions: List[Question] = []
        self.active_sessions: Dict[str, QuizSession] = {}
        self.load_questions()
    
    def load_questions(self):
        """Load questions from JSON file"""
        try:
            with open(Config.QUESTIONS_FILE, 'r', encoding='utf-8') as f:
                questions_data = json.load(f)
                self.questions = [Question(**q) for q in questions_data]
            print(f"Loaded {len(self.questions)} questions from {Config.QUESTIONS_FILE}")
        except FileNotFoundError:
            print(f"Questions file not found: {Config.QUESTIONS_FILE}")
            self.questions = []
        except json.JSONDecodeError as e:
            print(f"Error parsing questions file: {e}")
            self.questions = []
    
    def get_all_questions(self) -> List[Question]:
        """Get all available questions"""
        return self.questions
    
    def get_questions_by_category(self, category: str) -> List[Question]:
        """Get questions filtered by category"""
        return [q for q in self.questions if q.category.lower() == category.lower()]
    
    def get_questions_by_difficulty(self, difficulty: str) -> List[Question]:
        """Get questions filtered by difficulty"""
        return [q for q in self.questions if q.difficulty.lower() == difficulty.lower()]
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        return list(set(q.category for q in self.questions))
    
    def get_difficulties(self) -> List[str]:
        """Get all unique difficulty levels"""
        return list(set(q.difficulty for q in self.questions))
    
    def create_quiz_session(self, 
                          num_questions: int = Config.DEFAULT_QUIZ_SIZE,
                          category: Optional[str] = None,
                          difficulty: Optional[str] = None) -> QuizSession:
        """Create a new quiz session with random questions"""
        
        # Filter questions based on criteria
        available_questions = self.questions
        
        if category:
            available_questions = [q for q in available_questions if q.category.lower() == category.lower()]
        
        if difficulty:
            available_questions = [q for q in available_questions if q.difficulty.lower() == difficulty.lower()]
        
        if not available_questions:
            raise ValueError("No questions available for the specified criteria")
        
        # Limit number of questions
        num_questions = min(num_questions, len(available_questions), Config.MAX_QUIZ_SIZE)
        
        # Select random questions
        selected_questions = random.sample(available_questions, num_questions)
        
        # Create session
        session_id = str(uuid.uuid4())
        session = QuizSession(
            session_id=session_id,
            questions=selected_questions,
            created_at=datetime.now().isoformat()
        )
        
        self.active_sessions[session_id] = session
        return session
    
    def get_quiz_session(self, session_id: str) -> Optional[QuizSession]:
        """Get an active quiz session"""
        return self.active_sessions.get(session_id)
    
    def submit_answer(self, session_id: str, question_id: int, selected_answer: int) -> bool:
        """Submit an answer for a question in a quiz session"""
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError("Quiz session not found")
        
        if session.is_completed:
            raise ValueError("Quiz session is already completed")
        
        # Check if question exists in session
        question_exists = any(q.id == question_id for q in session.questions)
        if not question_exists:
            raise ValueError("Question not found in this quiz session")
        
        # Check if answer already exists for this question
        existing_response = next((r for r in session.responses if r.question_id == question_id), None)
        if existing_response:
            # Update existing response
            existing_response.selected_answer = selected_answer
        else:
            # Add new response
            response = QuizResponse(question_id=question_id, selected_answer=selected_answer)
            session.responses.append(response)
        
        return True
    
    def complete_quiz(self, session_id: str) -> QuizSummary:
        """Complete a quiz session and return results"""
        session = self.active_sessions.get(session_id)
        if not session:
            raise ValueError("Quiz session not found")
        
        session.is_completed = True
        
        # Calculate results
        results = []
        correct_count = 0
        
        for question in session.questions:
            response = next((r for r in session.responses if r.question_id == question.id), None)
            selected_answer = response.selected_answer if response else -1
            is_correct = selected_answer == question.correct_answer
            
            if is_correct:
                correct_count += 1
            
            result = QuizResult(
                question_id=question.id,
                question=question.question,
                options=question.options,
                selected_answer=selected_answer,
                correct_answer=question.correct_answer,
                is_correct=is_correct,
                category=question.category,
                difficulty=question.difficulty
            )
            results.append(result)
        
        total_questions = len(session.questions)
        wrong_count = total_questions - correct_count
        score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        summary = QuizSummary(
            total_questions=total_questions,
            correct_answers=correct_count,
            wrong_answers=wrong_count,
            score_percentage=round(score_percentage, 2),
            results=results
        )
        
        return summary
    
    def get_question_by_id(self, question_id: int) -> Optional[Question]:
        """Get a specific question by ID"""
        return next((q for q in self.questions if q.id == question_id), None)
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions (basic cleanup)"""
        # This is a basic implementation - in production you'd want proper session management
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.active_sessions.items():
            if session.created_at:
                created_time = datetime.fromisoformat(session.created_at)
                if (current_time - created_time).seconds > Config.SESSION_TIMEOUT:
                    expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
        
        return len(expired_sessions)