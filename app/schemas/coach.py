from typing import Optional

from pydantic import BaseModel


class FeedbackRequest(BaseModel):
    text: str
    level: Optional[str] = None
    focus: Optional[str] = None
    known_words: Optional[list[str]] = None


class FeedbackResponse(BaseModel):
    corrected: str
    explanation: str
    tips: list[str]


class RoleplayRequest(BaseModel):
    scenario: str
    level: Optional[str] = None
    user_input: Optional[str] = None
    formality: Optional[str] = None
    known_words: Optional[list[str]] = None
    user_id: Optional[int] = None


class RoleplayResponse(BaseModel):
    reply: str
    suggested_reply: str
    new_words: list[str]
