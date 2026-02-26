from fastapi import APIRouter, Query

from app.services.streaks import compute_streaks
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/stats", tags=["stats"])


def _count(table: str, **filters):
    supabase = get_supabase_client()
    query = supabase.table(table).select("id", count="exact")
    for key, value in filters.items():
        query = query.eq(key, value)
    result = query.execute()
    return result.count or 0


@router.get("/overview")
def overview(user_id: int = Query(...)):
    supabase = get_supabase_client()
    totals = {
        "words": _count("words"),
        "grammar": _count("grammar"),
        "expressions": _count("expressions"),
        "scenarios": _count("scenarios"),
    }

    mastered_words = (
        supabase.table("user_word_state")
        .select("id", count="exact")
        .eq("user_id", user_id)
        .gte("mastery_score", 0.8)
        .execute()
    )
    mastered_count = mastered_words.count or 0

    logs = (
        supabase.table("study_log")
        .select("timestamp")
        .eq("user_id", user_id)
        .limit(2000)
        .execute()
    )
    timestamps = [row["timestamp"] for row in logs.data]
    streaks = compute_streaks(timestamps)

    return {
        "status": "ok",
        "data": {
            "totals": totals,
            "mastered_words": mastered_count,
            "streaks": streaks,
        },
    }
