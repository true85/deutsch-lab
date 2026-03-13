from datetime import date

from fastapi import APIRouter, HTTPException, Query

from app.schemas.scenarios import ScenarioCreate, ScenarioUpdate
from app.services.sm2 import sm2_schedule
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.post("")
def create_scenario(payload: ScenarioCreate):
    supabase = get_supabase_client()
    result = supabase.table("scenarios").insert(payload.model_dump()).execute()
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to create scenario")
    return {"status": "ok", "data": result.data[0]}


@router.get("")
def list_scenarios(
    level_min: str | None = Query(default=None),
    level_max: str | None = Query(default=None),
    situation: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    supabase = get_supabase_client()
    query = supabase.table("scenarios").select("*").range(offset, offset + limit - 1)
    if level_min:
        query = query.eq("level_min", level_min)
    if level_max:
        query = query.eq("level_max", level_max)
    if situation:
        query = query.eq("situation", situation)
    result = query.execute()
    return {"status": "ok", "data": result.data}


@router.get("/{scenario_id}")
def get_scenario(scenario_id: int):
    supabase = get_supabase_client()
    result = supabase.table("scenarios").select("*").eq("id", scenario_id).limit(1).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {"status": "ok", "data": result.data[0]}


@router.put("/{scenario_id}")
def update_scenario(scenario_id: int, payload: ScenarioUpdate):
    supabase = get_supabase_client()
    data = payload.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = supabase.table("scenarios").update(data).eq("id", scenario_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {"status": "ok", "data": result.data[0]}


@router.delete("/{scenario_id}")
def delete_scenario(scenario_id: int):
    supabase = get_supabase_client()
    result = supabase.table("scenarios").delete().eq("id", scenario_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {"status": "ok", "data": result.data[0]}


@router.post("/{scenario_id}/practice")
def practice_scenario(
    scenario_id: int,
    user_id: int = Query(...),
    quality: int = Query(default=4, ge=0, le=5),
):
    supabase = get_supabase_client()
    scenario_check = supabase.table("scenarios").select("id").eq("id", scenario_id).limit(1).execute()
    if not scenario_check.data:
        raise HTTPException(status_code=404, detail="Scenario not found")

    today = date.today().isoformat()
    existing = (
        supabase.table("user_scenario_state")
        .select("*")
        .eq("user_id", user_id)
        .eq("scenario_id", scenario_id)
        .limit(1)
        .execute()
    )

    if existing.data:
        state = existing.data[0]
        schedule = sm2_schedule(
            quality,
            state.get("reps", 0),
            state.get("interval_days", 0),
            state.get("ease_factor", 2.7),
        )
        if quality == 5:
            new_mastery = 1.0
        else:
            new_mastery = min(0.9, state.get("mastery_score", 0.0) + 0.1 * (quality / 5))
        update_data = {
            "times_practiced": state.get("times_practiced", 0) + 1,
            "last_practiced": today,
            "reps": schedule["reps"],
            "interval_days": schedule["interval_days"],
            "ease_factor": schedule["ease_factor"],
            "next_review": schedule["next_review"],
            "mastery_score": round(new_mastery, 4),
        }
        result = supabase.table("user_scenario_state").update(update_data).eq("id", state["id"]).execute()
    else:
        schedule = sm2_schedule(quality, 0, 0, 2.7)
        insert_data = {
            "user_id": user_id,
            "scenario_id": scenario_id,
            "times_practiced": 1,
            "last_practiced": today,
            "reps": schedule["reps"],
            "interval_days": schedule["interval_days"],
            "ease_factor": schedule["ease_factor"],
            "next_review": schedule["next_review"],
            "mastery_score": 1.0 if quality == 5 else round(0.1 * (quality / 5), 4),
        }
        result = supabase.table("user_scenario_state").insert(insert_data).execute()

    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to record practice")
    return {"status": "ok", "data": result.data[0]}
