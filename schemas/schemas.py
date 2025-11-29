# schemas.py
from pydantic import BaseModel

class FeedbackResponse(BaseModel):
    feedback: str
    error: float
    is_correct: bool
    elapsed_time: float = 0.0