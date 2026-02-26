from fastapi import APIRouter, Query

from app.services.streaks import compute_streaks
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/achievements", tags=["achievements"])


def _count(table: str, **filters):
    supabase = get_supabase_client()
    query = supabase.table(table).select("id", count="exact")
    for key, value in filters.items():
        query = query.eq(key, value)
    result = query.execute()
    return result.count or 0


@router.get("")
def achievements(user_id: int = Query(...)):
    supabase = get_supabase_client()
    mastered_words = (
        supabase.table("user_word_state")
        .select("id", count="exact")
        .eq("user_id", user_id)
        .gte("mastery_score", 0.8)
        .execute()
    ).count or 0

    mastered_grammar = (
        supabase.table("user_grammar_state")
        .select("id", count="exact")
        .eq("user_id", user_id)
        .gte("mastery_score", 0.8)
        .execute()
    ).count or 0

    expressions_learned = _count("user_expression_state", user_id=user_id)

    logs = (
        supabase.table("study_log")
        .select("timestamp")
        .eq("user_id", user_id)
        .limit(2000)
        .execute()
    )
    streaks = compute_streaks([row["timestamp"] for row in logs.data])

    badges = [
        {
            "id": "words_100",
            "label": "Word Builder",
            "desc": "Mastered 100 words",
            "unlocked": mastered_words >= 100,
        },
        {
            "id": "words_500",
            "label": "Word Architect",
            "desc": "Mastered 500 words",
            "unlocked": mastered_words >= 500,
        },
        {
            "id": "grammar_50",
            "label": "Grammar Guard",
            "desc": "Mastered 50 grammar rules",
            "unlocked": mastered_grammar >= 50,
        },
        {
            "id": "expressions_200",
            "label": "Phrase Collector",
            "desc": "Learned 200 expressions",
            "unlocked": expressions_learned >= 200,
        },
        {
            "id": "streak_7",
            "label": "7-Day Streak",
            "desc": "Studied 7 days in a row",
            "unlocked": streaks["current"] >= 7,
        },
        {
            "id": "streak_30",
            "label": "30-Day Streak",
            "desc": "Studied 30 days in a row",
            "unlocked": streaks["current"] >= 30,
        },
    ]
    return {"status": "ok", "data": {"badges": badges, "streaks": streaks}}
