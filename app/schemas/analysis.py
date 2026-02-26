from typing import Optional

from pydantic import BaseModel


class SentenceAnalyzeRequest(BaseModel):
    sentence: str
    user_id: Optional[int] = None
    level_hint: Optional[str] = None
    save: bool = False


class AnalyzedWord(BaseModel):
    surface: str
    lemma: str
    word_id: Optional[int] = None
    source: str


class SentenceAnalyzeResponse(BaseModel):
    sentence: str
    level: Optional[str] = None
    words: list[AnalyzedWord]
    grammar: list[dict]
    saved: bool
    expression_id: Optional[int] = None
