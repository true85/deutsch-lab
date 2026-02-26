from fastapi import APIRouter, HTTPException, Query

from app.schemas.transfer import TransferPayload
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/transfer", tags=["transfer"])


STATE_TABLES = {
    "user_word_state": ("user_id", "word_id"),
    "user_grammar_state": ("user_id", "grammar_id"),
    "user_expression_state": ("user_id", "expression_id"),
    "user_scenario_state": ("user_id", "scenario_id"),
}


@router.get("/export")
def export_user(user_id: int = Query(...)):
    supabase = get_supabase_client()
    data = {}
    for table in STATE_TABLES:
        rows = supabase.table(table).select("*").eq("user_id", user_id).execute().data
        data[table] = rows
    logs = supabase.table("study_log").select("*").eq("user_id", user_id).execute().data
    data["study_log"] = logs
    return {"status": "ok", "data": data}


@router.post("/import")
def import_user(payload: TransferPayload):
    if payload.mode not in {"upsert", "insert"}:
        raise HTTPException(status_code=400, detail="mode must be upsert|insert")
    supabase = get_supabase_client()
    results = {}

    for table, conflict_keys in STATE_TABLES.items():
        rows = payload.data.get(table, [])
        cleaned = []
        for row in rows:
            row = dict(row)
            row.pop("id", None)
            row["user_id"] = payload.user_id
            cleaned.append(row)
        if not cleaned:
            results[table] = 0
            continue
        if payload.mode == "upsert":
            on_conflict = ",".join(conflict_keys)
            resp = supabase.table(table).upsert(cleaned, on_conflict=on_conflict).execute()
        else:
            resp = supabase.table(table).insert(cleaned).execute()
        results[table] = len(resp.data)

    logs = payload.data.get("study_log", [])
    if logs:
        cleaned_logs = []
        for row in logs:
            row = dict(row)
            row.pop("id", None)
            row["user_id"] = payload.user_id
            cleaned_logs.append(row)
        resp = supabase.table("study_log").insert(cleaned_logs).execute()
        results["study_log"] = len(resp.data)
    else:
        results["study_log"] = 0

    return {"status": "ok", "data": results}
