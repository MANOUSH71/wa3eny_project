from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Channel(str, Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    LOGIN_PAGE = "login_page"

class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class ScenarioRequest(BaseModel):
    department: Optional[str] = None
    sector: Optional[str] = None
    difficulty: Difficulty = Difficulty.MEDIUM

class Question(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str

class ScenarioResponse(BaseModel):
    channel: Channel
    sender_name: str
    sender_handle: str
    title: str
    message: str
    is_phishing: bool
    red_flags: List[str]
    questions: List[Question]
    correct_action: str
    explanation: str

class ClassificationRequest(BaseModel):
    scenario_id: Optional[str] = None
    user_classification: bool
    selected_flags: List[str] = []

class ClassificationResult(BaseModel):
    correct_classification: bool
    score: int
    feedback: str
    flag_analysis: dict
