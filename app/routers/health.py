from fastapi import APIRouter, HTTPException

from app.supabase_client import get_supabase_client

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/supabase-health")
def supabase_health():
    try:
        supabase = get_supabase_client()
        result = supabase.table("words").select("id").limit(1).execute()
        return {"status": "ok", "rows_checked": len(result.data)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
