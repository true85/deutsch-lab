import re
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.schemas.analysis import (
    AnalyzedWord,
    SentenceAnalyzeRequest,
    SentenceAnalyzeResponse,
)
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/analysis", tags=["analysis"])

# 하이픈 연결 복합어 포함 (예: Vor-Ort-Termin, Nord-Süd-Dialog)
_TOKEN_RE = re.compile(r"[A-Za-zÄÖÜäöüß]+(?:-[A-Za-zÄÖÜäöüß]+)*")

# 단독 하이픈 연결 토큰을 구성 단어로 분리할 때 사용
_HYPHEN_SPLIT_RE = re.compile(r"-")

# 독일어 약어 패턴 (한 글자 + 마침표): z.B., d.h., u.a. 등 — 이미 토큰화 대상 아님
# 단어 끝 약어 마침표 제거용
_ABBR_RE = re.compile(r"\b([A-ZÄÖÜ][a-z]?)\.(?=\s|$)")


def _tokenize(text: str) -> list[str]:
    """독일어 텍스트를 단어 토큰 목록으로 변환.

    - 하이픈 연결 복합어를 단일 토큰으로 유지 (Vor-Ort-Termin → ["Vor-Ort-Termin"])
    - 약어 마침표를 미리 공백으로 치환하여 오분리 방지
    - 단일 알파벳 토큰(관사 대체 등) 제외
    """
    # 약어 마침표 제거 (z.B. → zB, 단어 경계 내 처리)
    cleaned = _ABBR_RE.sub(r"\1", text)
    tokens = _TOKEN_RE.findall(cleaned)
    # 단일 문자 토큰 제거 (독일어에서 의미 없는 단독 알파벳)
    return [t for t in tokens if len(t) > 1]


def _compound_lemma(token: str) -> str:
    """하이픈 복합어의 기본 표제어 반환.

    독일어 복합어는 마지막 구성 요소가 핵심 의미를 담으므로
    하이픈이 있으면 마지막 구성 요소의 소문자형을 반환.
    예: Vor-Ort-Termin → termin, Nord-Süd-Dialog → dialog
    """
    parts = _HYPHEN_SPLIT_RE.split(token)
    return parts[-1].lower()


def _find_word_by_form(token: str) -> Optional[int]:
    supabase = get_supabase_client()
    # Prefer explicit word_forms match
    result = (
        supabase.table("word_forms")
        .select("word_id")
        .ilike("form", token)
        .limit(1)
        .execute()
    )
    if result.data:
        return result.data[0]["word_id"]
    return None


def _find_word_by_lemma(lemma: str) -> Optional[int]:
    supabase = get_supabase_client()
    result = (
        supabase.table("words").select("id").ilike("lemma", lemma).limit(1).execute()
    )
    if result.data:
        return result.data[0]["id"]
    return None


def _insert_word(lemma: str, level: str) -> int:
    supabase = get_supabase_client()
    payload = {
        "lemma": lemma,
        "part_of_speech": "unknown",
        "level": level,
    }
    result = supabase.table("words").insert(payload).execute()
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to insert word")
    return result.data[0]["id"]


def _upsert_expression(sentence: str, level: str) -> int:
    supabase = get_supabase_client()
    existing = (
        supabase.table("expressions").select("id").eq("german", sentence).limit(1).execute()
    )
    if existing.data:
        return existing.data[0]["id"]
    result = supabase.table("expressions").insert(
        {"german": sentence, "level": level}
    ).execute()
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to insert expression")
    return result.data[0]["id"]


def _link_expression_words(expression_id: int, word_ids: list[int]) -> None:
    supabase = get_supabase_client()
    rows = [{"expression_id": expression_id, "word_id": word_id} for word_id in word_ids]
    if not rows:
        return
    supabase.table("expression_words").upsert(
        rows, on_conflict="expression_id,word_id"
    ).execute()


@router.post("/sentence", response_model=SentenceAnalyzeResponse)
def analyze_sentence(payload: SentenceAnalyzeRequest):
    sentence = payload.sentence.strip()
    if not sentence:
        raise HTTPException(status_code=400, detail="sentence is required")
    level = payload.level_hint or "A1"

    tokens = _tokenize(sentence)
    words: list[AnalyzedWord] = []
    word_ids: list[int] = []
    for token in tokens:
        lemma = _compound_lemma(token)
        word_id = _find_word_by_form(token)
        source = "form"
        if word_id is None:
            word_id = _find_word_by_lemma(lemma)
            source = "lemma" if word_id is not None else "new"
        if word_id is None and payload.save:
            word_id = _insert_word(lemma, level)
        if word_id is not None:
            word_ids.append(word_id)
        words.append(
            AnalyzedWord(
                surface=token,
                lemma=lemma,
                word_id=word_id,
                source=source,
            )
        )

    expression_id = None
    if payload.save:
        expression_id = _upsert_expression(sentence, level)
        _link_expression_words(expression_id, word_ids)

    return SentenceAnalyzeResponse(
        sentence=sentence,
        level=level,
        words=words,
        grammar=[],
        saved=payload.save,
        expression_id=expression_id,
    )
