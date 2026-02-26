import json

from fastapi import APIRouter, HTTPException

from app.llm.openai_client import chat_json
from app.llm.prompts import FEEDBACK_PROMPT, ROLEPLAY_PROMPT, SYSTEM_BASE
from app.schemas.coach import FeedbackRequest, FeedbackResponse, RoleplayRequest, RoleplayResponse
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/coach", tags=["coach"])


@router.post("/feedback", response_model=FeedbackResponse)
def feedback(payload: FeedbackRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="text is required")
    user_prompt = {
        "text": payload.text,
        "level": payload.level,
        "focus": payload.focus,
        "known_words": payload.known_words,
    }
    result = chat_json(SYSTEM_BASE + "\n" + FEEDBACK_PROMPT, json.dumps(user_prompt, ensure_ascii=False))
    if "corrected" not in result:
        raise HTTPException(status_code=502, detail="LLM response invalid")
    return result


@router.post("/roleplay", response_model=RoleplayResponse)
def roleplay(payload: RoleplayRequest):
    if not payload.scenario.strip():
        raise HTTPException(status_code=400, detail="scenario is required")

    known_words = payload.known_words
    if known_words is None and payload.user_id is not None:
        supabase = get_supabase_client()
        states = (
            supabase.table("user_word_state")
            .select("word_id")
            .eq("user_id", payload.user_id)
            .gte("mastery_score", 0.5)
            .execute()
        )
        if states.data:
            word_ids = [row["word_id"] for row in states.data]
            words = supabase.table("words").select("lemma").in_("id", word_ids).execute()
            known_words = [row["lemma"] for row in words.data]

    user_prompt = {
        "scenario": payload.scenario,
        "level": payload.level,
        "user_input": payload.user_input,
        "formality": payload.formality,
        "known_words": known_words,
    }
    result = chat_json(SYSTEM_BASE + "\n" + ROLEPLAY_PROMPT, json.dumps(user_prompt, ensure_ascii=False))
    if "reply" not in result:
        raise HTTPException(status_code=502, detail="LLM response invalid")
    return result
