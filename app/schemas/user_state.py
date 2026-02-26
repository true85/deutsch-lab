from typing import Optional

from pydantic import BaseModel


class UserWordStateBase(BaseModel):
    user_id: int
    word_id: int
    first_learned: Optional[str] = None
    last_reviewed: Optional[str] = None
    next_review: Optional[str] = None
    times_reviewed: int = 0
    mastery_score: float = 0.0
    ease_factor: float = 2.7
    interval_days: int = 0
    reps: int = 0
    success_count: int = 0
    fail_count: int = 0


class UserWordStateCreate(UserWordStateBase):
    pass


class UserWordStateUpdate(BaseModel):
    first_learned: Optional[str] = None
    last_reviewed: Optional[str] = None
    next_review: Optional[str] = None
    times_reviewed: Optional[int] = None
    mastery_score: Optional[float] = None
    ease_factor: Optional[float] = None
    interval_days: Optional[int] = None
    reps: Optional[int] = None
    success_count: Optional[int] = None
    fail_count: Optional[int] = None


class UserGrammarStateBase(BaseModel):
    user_id: int
    grammar_id: int
    first_learned: Optional[str] = None
    last_reviewed: Optional[str] = None
    next_review: Optional[str] = None
    times_reviewed: int = 0
    mastery_score: float = 0.0
    ease_factor: float = 2.7
    interval_days: int = 0
    reps: int = 0
    success_count: int = 0
    fail_count: int = 0


class UserGrammarStateCreate(UserGrammarStateBase):
    pass


class UserGrammarStateUpdate(BaseModel):
    first_learned: Optional[str] = None
    last_reviewed: Optional[str] = None
    next_review: Optional[str] = None
    times_reviewed: Optional[int] = None
    mastery_score: Optional[float] = None
    ease_factor: Optional[float] = None
    interval_days: Optional[int] = None
    reps: Optional[int] = None
    success_count: Optional[int] = None
    fail_count: Optional[int] = None


class UserExpressionStateBase(BaseModel):
    user_id: int
    expression_id: int
    first_learned: Optional[str] = None
    last_reviewed: Optional[str] = None
    next_review: Optional[str] = None
    times_reviewed: int = 0
    mastery_score: float = 0.0
    ease_factor: float = 2.7
    interval_days: int = 0
    reps: int = 0


class UserExpressionStateCreate(UserExpressionStateBase):
    pass


class UserExpressionStateUpdate(BaseModel):
    first_learned: Optional[str] = None
    last_reviewed: Optional[str] = None
    next_review: Optional[str] = None
    times_reviewed: Optional[int] = None
    mastery_score: Optional[float] = None
    ease_factor: Optional[float] = None
    interval_days: Optional[int] = None
    reps: Optional[int] = None


class UserScenarioStateBase(BaseModel):
    user_id: int
    scenario_id: int
    times_practiced: int = 0
    last_practiced: Optional[str] = None
    mastery_score: float = 0.0
    ease_factor: float = 2.7
    interval_days: int = 0
    reps: int = 0
    next_review: Optional[str] = None


class UserScenarioStateCreate(UserScenarioStateBase):
    pass


class UserScenarioStateUpdate(BaseModel):
    times_practiced: Optional[int] = None
    last_practiced: Optional[str] = None
    mastery_score: Optional[float] = None
    ease_factor: Optional[float] = None
    interval_days: Optional[int] = None
    reps: Optional[int] = None
    next_review: Optional[str] = None
