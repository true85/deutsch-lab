from typing import Optional

from pydantic import BaseModel


class ExpressionBase(BaseModel):
    german: str
    level: str
    korean: Optional[str] = None
    type: Optional[str] = None
    formality: Optional[str] = None
    situation: Optional[str] = None
    context: Optional[str] = None


class ExpressionCreate(ExpressionBase):
    pass


class ExpressionUpdate(BaseModel):
    german: Optional[str] = None
    level: Optional[str] = None
    korean: Optional[str] = None
    type: Optional[str] = None
    formality: Optional[str] = None
    situation: Optional[str] = None
    context: Optional[str] = None


class ExpressionOut(ExpressionBase):
    id: int
