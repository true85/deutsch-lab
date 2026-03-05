import json
import random
from datetime import date, datetime

from fastapi import APIRouter, HTTPException

from app.llm.openai_client import chat_json
from app.llm.prompts import (
    SYSTEM_BASE,
    TEACHER_CHAT_PROMPT,
    TEACHER_CHAT_SYSTEM_PROMPT,
    TEACHER_GENERATE_GRAMMAR_PROMPT,
    TEACHER_GENERATE_SCENARIO_PROMPT,
    TEACHER_GENERATE_SENTENCES_PROMPT,
    TEACHER_GENERATE_WORDS_PROMPT,
)
from app.routers.recommend import _get_user_avg_mastery, _get_user_current_level
from app.schemas.teacher import ChatRequest, GenerateGrammarRequest, GenerateScenarioRequest, GenerateSentencesRequest, GenerateWordsRequest
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/teacher", tags=["teacher"])


def _build_user_profile(user_id: int) -> dict:
    supabase = get_supabase_client()

    current_level = _get_user_current_level(user_id)
    avg_mastery = _get_user_avg_mastery(user_id)

    # 아는 단어 (mastery >= 0.5)
    known_states = (
        supabase.table("user_word_state")
        .select("word_id")
        .eq("user_id", user_id)
        .gte("mastery_score", 0.5)
        .execute()
    )
    known_lemmas: list[str] = []
    if known_states.data:
        known_ids = [row["word_id"] for row in known_states.data]
        words = supabase.table("words").select("lemma").in_("id", known_ids).execute()
        known_lemmas = [row["lemma"] for row in words.data if row["lemma"]]

    # 취약 단어 (mastery_score > 0 AND < 0.5 — 복습했지만 약한 단어만)
    weak_word_states = (
        supabase.table("user_word_state")
        .select("word_id")
        .eq("user_id", user_id)
        .gt("mastery_score", 0.0)
        .lt("mastery_score", 0.5)
        .execute()
    )
    weak_word_lemmas: list[str] = []
    if weak_word_states.data:
        weak_ids = [row["word_id"] for row in weak_word_states.data]
        weak_words = supabase.table("words").select("lemma").in_("id", weak_ids).execute()
        weak_word_lemmas = [row["lemma"] for row in weak_words.data if row["lemma"]]

    # 취약 문법 (mastery_score < 0.5)
    grammar_states = (
        supabase.table("user_grammar_state")
        .select("grammar_id,mastery_score")
        .eq("user_id", user_id)
        .lt("mastery_score", 0.5)
        .execute()
    )
    weak_grammar_rules: list[dict] = []
    if grammar_states.data:
        weak_grammar_ids = [row["grammar_id"] for row in grammar_states.data]
        grammar_rows = (
            supabase.table("grammar")
            .select("rule_name,explanation")
            .in_("id", weak_grammar_ids)
            .execute()
        )
        weak_grammar_rules = grammar_rows.data

    # 오늘 복습 예정 단어 (SM-2 next_review <= today)
    today_str = date.today().isoformat()
    review_states = (
        supabase.table("user_word_state")
        .select("word_id")
        .eq("user_id", user_id)
        .lte("next_review", today_str)
        .execute()
    )
    review_due_lemmas: list[str] = []
    if review_states.data:
        review_ids = [row["word_id"] for row in review_states.data]
        review_words = supabase.table("words").select("lemma").in_("id", review_ids).execute()
        review_due_lemmas = [row["lemma"] for row in review_words.data]

    return {
        "current_level": current_level,
        "avg_mastery": avg_mastery,
        "known_lemmas": known_lemmas,
        "weak_word_lemmas": weak_word_lemmas,
        "weak_grammar_rules": weak_grammar_rules,
        "review_due_lemmas": review_due_lemmas,
    }


@router.post("/generate-words")
def generate_words(req: GenerateWordsRequest):
    profile = _build_user_profile(req.user_id)
    user_prompt = {
        "current_level": profile["current_level"],
        "avg_mastery": profile["avg_mastery"],
        "weak_word_lemmas": profile["weak_word_lemmas"][:20],
        "known_lemmas": profile["known_lemmas"],
        "count": req.count,
        "theme": req.theme,
    }
    result = chat_json(SYSTEM_BASE + TEACHER_GENERATE_WORDS_PROMPT, json.dumps(user_prompt, ensure_ascii=False))
    if "words" not in result:
        raise HTTPException(status_code=502, detail="LLM이 올바른 응답을 반환하지 않았습니다.")
    return {"status": "ok", "data": result}


# 독일어 불용어 (단어 버튼에서 제외)
_DE_STOPWORDS = {
    "der", "die", "das", "ein", "eine", "einen", "einem", "einer", "eines",
    "des", "dem", "den", "ich", "du", "er", "sie", "es", "wir", "ihr",
    "in", "aus", "von", "zu", "mit", "nach", "bei", "seit", "bis",
    "für", "ohne", "durch", "gegen", "um", "an", "auf", "über", "unter",
    "und", "oder", "aber", "denn", "sondern", "nicht", "auch", "noch",
    "ja", "nein", "bitte", "danke", "ist", "bin", "bist", "sind", "seid",
}


def _fallback_words(german: str, known_lower: set[str], supabase) -> list[dict]:
    """LLM이 words를 반환하지 않을 때 문장에서 직접 단어 추출."""
    import re
    tokens = re.findall(r"[A-Za-zÄäÖöÜüß]+", german)
    seen: set[str] = set()
    words = []
    for token in tokens:
        lower = token.lower()
        if lower in _DE_STOPWORDS or lower in seen:
            continue
        seen.add(lower)
        row = supabase.table("words").select("id,lemma,translation,part_of_speech,gender,plural").ilike("lemma", token).limit(1).execute()
        if row.data:
            w = row.data[0]
            words.append({
                "german": w["lemma"],
                "translation": w.get("translation", ""),
                "part_of_speech": w.get("part_of_speech", ""),
                "gender": w.get("gender"),
                "plural": w.get("plural"),
                "is_new": lower not in known_lower,
                "word_id": w["id"],
            })
        else:
            words.append({
                "german": token,
                "translation": "",
                "part_of_speech": "",
                "gender": None,
                "plural": None,
                "is_new": lower not in known_lower,
                "word_id": None,
            })
    return words


_SENTENCE_THEMES = [
    "일상 대화", "카페/식당", "쇼핑", "여행", "직장/학교", "날씨",
    "가족", "취미", "건강/병원", "교통", "집/이사", "친구 관계",
]


def _upsert_word_state(user_id: int, word_id: int, today: str, supabase) -> None:
    try:
        supabase.table("user_word_state").upsert({
            "user_id": user_id,
            "word_id": word_id,
            "mastery_score": 0.0,
            "next_review": today,
        }, ignore_duplicates=True).execute()
    except Exception:
        pass


def _save_word_to_db(w: dict, current_level: str, supabase) -> int | None:
    """is_new 단어를 words 테이블에 저장하고 word_id 반환."""
    existing = supabase.table("words").select("id").ilike("lemma", w["german"]).limit(1).execute()
    if existing.data:
        return existing.data[0]["id"]
    try:
        inserted = supabase.table("words").insert({
            "lemma": w["german"],
            "part_of_speech": w.get("part_of_speech", ""),
            "translation": w.get("translation", ""),
            "gender": w.get("gender"),
            "plural": w.get("plural"),
            "level": current_level,
            "frequency": "common",
        }).execute()
        return inserted.data[0]["id"] if inserted.data else None
    except Exception:
        return None



@router.post("/generate-grammar")
def generate_grammar(req: GenerateGrammarRequest):
    supabase = get_supabase_client()
    level = req.level or _get_user_current_level(req.user_id)

    existing = supabase.table("grammar").select("rule_name").eq("level", level).execute()
    existing_names = [row["rule_name"] for row in existing.data] if existing.data else []

    user_prompt = {
        "current_level": level,
        "existing_rule_names": existing_names,
        "count": req.count,
    }
    result = chat_json(SYSTEM_BASE + TEACHER_GENERATE_GRAMMAR_PROMPT, json.dumps(user_prompt, ensure_ascii=False))
    if "grammar_rules" not in result:
        raise HTTPException(status_code=502, detail="LLM이 올바른 응답을 반환하지 않았습니다.")

    saved, skipped = 0, 0
    saved_rules = []
    for rule in result["grammar_rules"]:
        rule_name = rule.get("rule_name", "")
        if not rule_name:
            skipped += 1
            continue
        # 중복 체크 (ilike)
        dup = supabase.table("grammar").select("id").ilike("rule_name", rule_name).limit(1).execute()
        if dup.data:
            skipped += 1
            continue
        try:
            raw_examples = rule.get("examples", [])
            examples_str = [
                f"{ex['german']} — {ex['korean']}" if isinstance(ex, dict) else str(ex)
                for ex in raw_examples
            ]
            inserted = supabase.table("grammar").insert({
                "rule_name": rule_name,
                "category": rule.get("category", "other"),
                "explanation": rule.get("explanation", ""),
                "examples": examples_str,
                "level": level,
            }).execute()
            if inserted.data:
                saved += 1
                saved_rules.append(inserted.data[0])
            else:
                skipped += 1
        except Exception:
            skipped += 1

    return {"status": "ok", "data": {"saved": saved, "skipped": skipped, "rules": saved_rules}}


@router.post("/generate-sentences")
def generate_sentences(req: GenerateSentencesRequest):
    supabase = get_supabase_client()
    profile = _build_user_profile(req.user_id)
    weak_grammar = profile["weak_grammar_rules"] or [
        {"rule_name": f"{profile['current_level']} general", "explanation": ""}
    ]

    session_theme = random.choice(_SENTENCE_THEMES)
    random_seed = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(100, 999))

    user_prompt = {
        "current_level": profile["current_level"],
        "weak_grammar_rules": weak_grammar[:5],
        "known_lemmas": profile["known_lemmas"][:50],
        "weak_word_lemmas": profile["weak_word_lemmas"][:20],
        "review_due_lemmas": profile.get("review_due_lemmas", [])[:15],
        "count": req.count,
        "session_theme": session_theme,
        "random_seed": random_seed,
    }
    result = chat_json(SYSTEM_BASE + TEACHER_GENERATE_SENTENCES_PROMPT, json.dumps(user_prompt, ensure_ascii=False))
    if "sentences" not in result:
        raise HTTPException(status_code=502, detail="LLM이 올바른 응답을 반환하지 않았습니다.")

    known_lower = {lemma.lower() for lemma in profile["known_lemmas"]}
    current_level = profile["current_level"]
    today = date.today().isoformat()

    for sentence in result["sentences"]:
        if not sentence.get("words"):
            words = _fallback_words(sentence["german"], known_lower, supabase)
            for w in words:
                if w.get("is_new") and w.get("word_id") is None:
                    w["word_id"] = _save_word_to_db(w, current_level, supabase)
                if w.get("is_new") and w.get("word_id"):
                    _upsert_word_state(req.user_id, w["word_id"], today, supabase)
            sentence["words"] = words
        else:
            for w in sentence["words"]:
                # 백엔드에서 is_new 재확인 (LLM 실수 보정)
                w["is_new"] = w.get("is_new", False) and w["german"].lower() not in known_lower
                if w.get("is_new"):
                    w["word_id"] = _save_word_to_db(w, current_level, supabase)
                    if w["word_id"]:
                        _upsert_word_state(req.user_id, w["word_id"], today, supabase)
                else:
                    row = supabase.table("words").select("id").ilike("lemma", w["german"]).limit(1).execute()
                    w["word_id"] = row.data[0]["id"] if row.data else None

        if "verbs" not in sentence:
            sentence["verbs"] = []

    return {"status": "ok", "data": result}


@router.post("/generate-scenario")
def generate_scenario(req: GenerateScenarioRequest):
    supabase = get_supabase_client()
    profile = _build_user_profile(req.user_id)
    user_prompt = {
        "current_level": profile["current_level"],
        "situation": req.situation,
        "seed_sentence": req.seed_sentence,
    }
    result = chat_json(SYSTEM_BASE + TEACHER_GENERATE_SCENARIO_PROMPT, json.dumps(user_prompt, ensure_ascii=False))
    if "dialogue_script" not in result:
        raise HTTPException(status_code=502, detail="LLM이 올바른 응답을 반환하지 않았습니다.")

    saved_id = None
    if req.save:
        try:
            inserted = supabase.table("scenarios").insert({
                "name": result.get("name", req.situation),
                "level_min": result.get("level_min", profile["current_level"]),
                "level_max": result.get("level_max", profile["current_level"]),
                "description": result.get("description", ""),
                "situation": result.get("situation", req.situation),
                "dialogue_script": result.get("dialogue_script", {}),
            }).execute()
            saved_id = inserted.data[0]["id"] if inserted.data else None
        except Exception:
            pass

    return {"status": "ok", "data": {"scenario": result, "saved_id": saved_id}}


@router.post("/chat")
def teacher_chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="메시지를 입력해주세요.")

    profile = _build_user_profile(req.user_id)
    known_sample = profile["known_lemmas"][:15]
    weak_grammar_sample = [r["rule_name"] for r in profile["weak_grammar_rules"]][:5]

    system_prompt = TEACHER_CHAT_SYSTEM_PROMPT + TEACHER_CHAT_PROMPT.format(
        current_level=profile["current_level"],
        known_sample=", ".join(known_sample) if known_sample else "없음",
        weak_grammar_sample=", ".join(weak_grammar_sample) if weak_grammar_sample else "없음",
        mode=req.mode,
    )
    history_dicts = [{"role": m.role, "content": m.content} for m in (req.history or [])]
    user_prompt = {
        "history": history_dicts[-10:],
        "current_message": req.message,
    }
    result = chat_json(system_prompt, json.dumps(user_prompt, ensure_ascii=False))
    if "reply" not in result:
        raise HTTPException(status_code=502, detail="LLM이 올바른 응답을 반환하지 않았습니다.")
    return {"status": "ok", "data": result}
