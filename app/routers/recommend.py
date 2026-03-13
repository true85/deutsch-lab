from collections import defaultdict
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import verify_api_key
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/recommend", tags=["recommend"], dependencies=[Depends(verify_api_key)])


def _get_known_word_ids(user_id: int, mastery_threshold: float):
    supabase = get_supabase_client()
    result = (
        supabase.table("user_word_state")
        .select("word_id")
        .eq("user_id", user_id)
        .gte("mastery_score", mastery_threshold)
        .execute()
    )
    return [row["word_id"] for row in result.data]


@router.get("/expressions")
def recommend_expressions(
    user_id: int = Query(...),
    mastery_threshold: float = Query(0.8, ge=0.0, le=1.0),
    min_ratio: float = Query(0.8, ge=0.0, le=1.0),
    include_known_only: bool = Query(False),
    limit: int = Query(20, ge=1, le=200),
):
    supabase = get_supabase_client()
    known_ids = _get_known_word_ids(user_id, mastery_threshold)
    if not known_ids:
        return {"status": "ok", "data": []}

    ew_known = (
        supabase.table("expression_words")
        .select("expression_id,word_id")
        .in_("word_id", known_ids)
        .execute()
    )
    if not ew_known.data:
        return {"status": "ok", "data": []}

    known_counts = defaultdict(int)
    for row in ew_known.data:
        known_counts[row["expression_id"]] += 1

    expression_ids = list(known_counts.keys())
    ew_all = (
        supabase.table("expression_words")
        .select("expression_id")
        .in_("expression_id", expression_ids)
        .execute()
    )
    total_counts = defaultdict(int)
    for row in ew_all.data:
        total_counts[row["expression_id"]] += 1

    candidates = []
    for expr_id, known_count in known_counts.items():
        total = total_counts.get(expr_id, 0)
        if total == 0:
            continue
        ratio = known_count / total
        if ratio >= min_ratio and (include_known_only or ratio < 1.0):
            candidates.append((expr_id, ratio))

    if not candidates:
        return {"status": "ok", "data": []}

    candidates.sort(key=lambda x: (-x[1], x[0]))
    top_ids = [expr_id for expr_id, _ in candidates[:limit]]
    result = (
        supabase.table("expressions")
        .select("*")
        .in_("id", top_ids)
        .execute()
    )
    return {"status": "ok", "data": result.data}


@router.get("/weak-words")
def recommend_weak_words(
    user_id: int = Query(...),
    limit: int = Query(20, ge=1, le=200),
):
    supabase = get_supabase_client()
    states = (
        supabase.table("user_word_state")
        .select("word_id,mastery_score")
        .eq("user_id", user_id)
        .gt("mastery_score", 0.0)
        .lt("mastery_score", 0.5)
        .order("mastery_score", desc=False)
        .limit(limit)
        .execute()
    )
    if not states.data:
        return {"status": "ok", "data": []}
    word_ids = [row["word_id"] for row in states.data]
    result = supabase.table("words").select("*").in_("id", word_ids).execute()
    return {"status": "ok", "data": result.data}


@router.get("/weak-grammar")
def recommend_weak_grammar(
    user_id: int = Query(...),
    limit: int = Query(20, ge=1, le=200),
):
    supabase = get_supabase_client()
    states = (
        supabase.table("user_grammar_state")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )
    if not states.data:
        return {"status": "ok", "data": []}

    scored = []
    for row in states.data:
        total = row.get("success_count", 0) + row.get("fail_count", 0)
        rate = row.get("success_count", 0) / total if total else 0.0
        scored.append((row["grammar_id"], rate))
    scored.sort(key=lambda x: x[1])
    top_ids = [gid for gid, _ in scored[:limit]]
    result = supabase.table("grammar").select("*").in_("id", top_ids).execute()
    return {"status": "ok", "data": result.data}


def _get_user_avg_mastery(user_id: int) -> float:
    supabase = get_supabase_client()
    states = (
        supabase.table("user_word_state")
        .select("mastery_score")
        .eq("user_id", user_id)
        .execute()
    )
    if not states.data:
        return 0.0
    scores = [row["mastery_score"] for row in states.data]
    return sum(scores) / len(scores)


def _get_user_current_level(user_id: int) -> str:
    supabase = get_supabase_client()
    states = (
        supabase.table("user_word_state")
        .select("word_id")
        .eq("user_id", user_id)
        .execute()
    )
    if not states.data:
        return "A1"
    word_ids = [row["word_id"] for row in states.data]
    words = supabase.table("words").select("level").in_("id", word_ids).execute()
    if not words.data:
        return "A1"
    level_order = ["A1", "A2", "B1", "B2", "C1", "C2"]
    level_counts: dict[str, int] = {}
    for row in words.data:
        lv = row.get("level", "A1")
        level_counts[lv] = level_counts.get(lv, 0) + 1
    return max(level_counts, key=lambda lv: (level_order.index(lv) if lv in level_order else 0))


@router.get("/today")
def recommend_today_bundle(
    user_id: int = Query(...),
    limit: int = Query(20, ge=1, le=200),
):
    supabase = get_supabase_client()
    today = date.today().isoformat()
    level_order = ["A1", "A2", "B1", "B2", "C1", "C2"]

    # Adaptive: 사용자 mastery 평균에 따라 레벨 조절
    avg_mastery = _get_user_avg_mastery(user_id)
    current_level = _get_user_current_level(user_id)
    current_idx = level_order.index(current_level) if current_level in level_order else 0

    words_due = (
        supabase.table("user_word_state")
        .select("word_id")
        .eq("user_id", user_id)
        .lte("next_review", today)
        .limit(limit)
        .execute()
    )
    word_ids = [row["word_id"] for row in words_due.data]

    # Adaptive: avg >= 0.7이면 다음 레벨 단어 20% 추가
    new_word_count = max(1, limit // 5)
    if avg_mastery >= 0.7 and current_idx < len(level_order) - 1:
        next_level = level_order[current_idx + 1]
        known_ids_set = set(word_ids)
        new_words = (
            supabase.table("words")
            .select("id")
            .eq("level", next_level)
            .limit(new_word_count * 3)
            .execute()
        )
        new_ids = [row["id"] for row in new_words.data if row["id"] not in known_ids_set]
        word_ids = word_ids + new_ids[:new_word_count]
    elif avg_mastery < 0.5:
        # avg < 0.5: 현재 레벨 복습 80% 유지 (이미 due words 위주로 구성됨)
        review_words = (
            supabase.table("words")
            .select("id")
            .eq("level", current_level)
            .limit(new_word_count)
            .execute()
        )
        extra_ids = [row["id"] for row in review_words.data if row["id"] not in set(word_ids)]
        word_ids = word_ids + extra_ids[:new_word_count]

    if not word_ids:
        return {"status": "ok", "data": {"words": [], "expressions": [], "scenarios": []}}

    word_rows = supabase.table("words").select("*").in_("id", word_ids).execute()
    expr_rows = (
        supabase.table("expression_words")
        .select("expression_id")
        .in_("word_id", word_ids)
        .execute()
    )
    expr_ids = list({row["expression_id"] for row in expr_rows.data})
    expressions = []
    if expr_ids:
        expressions = (
            supabase.table("expressions").select("*").in_("id", expr_ids).execute().data
        )

    # 복습 필요한 시나리오 조회
    due_scenario_states = (
        supabase.table("user_scenario_state")
        .select("scenario_id")
        .eq("user_id", user_id)
        .lte("next_review", today)
        .limit(limit // 4 + 1)
        .execute()
    )
    scenario_ids = [row["scenario_id"] for row in due_scenario_states.data]

    # 신규 시나리오 20% 추가
    new_scenario_count = max(1, (limit // 4 + 1) // 5)
    known_scenario_ids_set = set(scenario_ids)
    new_scenarios = (
        supabase.table("scenarios")
        .select("id")
        .limit(new_scenario_count * 3)
        .execute()
    )
    new_scenario_ids = [row["id"] for row in new_scenarios.data if row["id"] not in known_scenario_ids_set]
    scenario_ids = scenario_ids + new_scenario_ids[:new_scenario_count]

    scenarios = []
    if scenario_ids:
        scenarios = supabase.table("scenarios").select("*").in_("id", scenario_ids).execute().data

    return {
        "status": "ok",
        "data": {
            "words": word_rows.data,
            "expressions": expressions,
            "scenarios": scenarios,
            "meta": {"avg_mastery": round(avg_mastery, 3), "current_level": current_level},
        },
    }


@router.get("/theme")
def recommend_theme(
    theme: str = Query(...),
    limit: int = Query(50, ge=1, le=200),
):
    supabase = get_supabase_client()
    words = supabase.table("words").select("*").eq("theme", theme).limit(limit).execute()
    expressions = (
        supabase.table("expressions")
        .select("*")
        .eq("situation", theme)
        .limit(limit)
        .execute()
    )
    return {"status": "ok", "data": {"words": words.data, "expressions": expressions.data}}
