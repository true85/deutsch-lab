from typing import Optional
from pydantic import BaseModel


class GenerateWordsRequest(BaseModel):
    user_id: int
    count: Optional[int] = 5
    theme: Optional[str] = None


class GeneratedWord(BaseModel):
    german: str
    part_of_speech: str
    gender: Optional[str] = None
    plural: Optional[str] = None
    translation: str
    example_sentence: str
    example_translation: str
    level: str


class GenerateSentencesRequest(BaseModel):
    user_id: int
    count: Optional[int] = 5


class SentenceWord(BaseModel):
    german: str
    translation: str
    part_of_speech: str  # verb | noun | adjective | adverb | other
    gender: Optional[str] = None  # 명사만 해당
    plural: Optional[str] = None
    is_new: bool
    word_id: Optional[int] = None  # DB에 저장된 id


class VerbConjugation(BaseModel):
    lemma: str
    present: dict[str, str]  # {"ich": "gehe", "du": "gehst", ...}


class GeneratedSentence(BaseModel):
    german: str
    korean: str
    grammar_focus: str
    blanked: Optional[str] = None
    hint: str
    words: list[SentenceWord] = []
    verbs: list[VerbConjugation] = []


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    user_id: int
    message: str
    history: Optional[list[ChatMessage]] = []
    mode: Optional[str] = "free"  # free | correction | vocab_drill
