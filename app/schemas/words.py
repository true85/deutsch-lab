from typing import Optional

from pydantic import BaseModel


class WordBase(BaseModel):
    lemma: str
    part_of_speech: str
    level: str
    translation: Optional[str] = None
    gender: Optional[str] = None
    plural: Optional[str] = None
    theme: Optional[str] = None
    frequency: Optional[str] = None


class WordCreate(WordBase):
    pass


class WordUpdate(BaseModel):
    lemma: Optional[str] = None
    part_of_speech: Optional[str] = None
    level: Optional[str] = None
    translation: Optional[str] = None
    gender: Optional[str] = None
    plural: Optional[str] = None
    theme: Optional[str] = None
    frequency: Optional[str] = None


class WordOut(WordBase):
    id: int
