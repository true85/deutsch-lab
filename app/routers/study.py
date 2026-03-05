from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import verify_api_key
from app.services.sm2 import sm2_schedule
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/study", tags=["study"], dependencies=[Depends(verify_api_key)])


@router.get("/review-today")
def review_today(
    user_id: int = Query(...),
    item_type: str = Query("word"),
    limit: int = Query(default=50, ge=1, le=200),
    with_details: bool = Query(False),
):
    table_map = {
        "word": "user_word_state",
        "grammar": "user_grammar_state",
        "expression": "user_expression_state",
    }
    if item_type not in table_map:
        raise HTTPException(status_code=400, detail="item_type must be word|grammar|expression")
    supabase = get_supabase_client()
    today = date.today().isoformat()
    result = (
        supabase.table(table_map[item_type])
        .select("*")
        .eq("user_id", user_id)
        .lte("next_review", today)
        .limit(limit)
        .execute()
    )
    if with_details and item_type == "word" and result.data:
        word_ids = [r["word_id"] for r in result.data]
        words_res = supabase.table("words").select("id,lemma,translation,level,part_of_speech").in_("id", word_ids).execute()
        word_map = {w["id"]: w for w in words_res.data}
        for r in result.data:
            r.update(word_map.get(r["word_id"], {}))
    return {"status": "ok", "data": result.data}


@router.post("/sm2")
def compute_sm2(
    quality: int = Query(..., ge=0, le=5),
    reps: int = Query(default=0, ge=0),
    interval_days: int = Query(default=0, ge=0),
    ease_factor: float = Query(default=2.7, ge=1.3),
):
    return {"status": "ok", "data": sm2_schedule(quality, reps, interval_days, ease_factor)}


@router.post("/review-word")
def review_word(
    state_id: int = Query(...),
    quality: int = Query(..., ge=0, le=5),
):
    supabase = get_supabase_client()
    result = supabase.table("user_word_state").select("*").eq("id", state_id).limit(1).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="State not found")
    state = result.data[0]
    schedule = sm2_schedule(
        quality,
        state.get("reps", 0),
        state.get("interval_days", 0),
        state.get("ease_factor", 2.7),
    )
    update_data = {
        "reps": schedule["reps"],
        "interval_days": schedule["interval_days"],
        "ease_factor": schedule["ease_factor"],
        "next_review": schedule["next_review"],
        "last_reviewed": date.today().isoformat(),
        "times_reviewed": state.get("times_reviewed", 0) + 1,
    }
    if quality < 3:
        update_data["fail_count"] = state.get("fail_count", 0) + 1
    else:
        update_data["success_count"] = state.get("success_count", 0) + 1
    updated = supabase.table("user_word_state").update(update_data).eq("id", state_id).execute()
    return {"status": "ok", "data": updated.data[0]}
