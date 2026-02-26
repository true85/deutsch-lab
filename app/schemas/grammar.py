from typing import Optional

from pydantic import BaseModel


class GrammarBase(BaseModel):
    rule_name: str
    level: str
    category: Optional[str] = None
    explanation: Optional[str] = None
    examples: Optional[list[str]] = None


class GrammarCreate(GrammarBase):
    pass


class GrammarUpdate(BaseModel):
    rule_name: Optional[str] = None
    level: Optional[str] = None
    category: Optional[str] = None
    explanation: Optional[str] = None
    examples: Optional[list[str]] = None


class GrammarOut(GrammarBase):
    id: int
