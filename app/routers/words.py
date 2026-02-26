from fastapi import APIRouter, HTTPException, Query

from app.schemas.words import WordCreate, WordUpdate
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/words", tags=["words"])


@router.post("")
def create_word(payload: WordCreate):
    supabase = get_supabase_client()
    result = supabase.table("words").insert(payload.model_dump()).execute()
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to create word")
    return {"status": "ok", "data": result.data[0]}


@router.get("")
def list_words(
    level: str | None = Query(default=None),
    theme: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    supabase = get_supabase_client()
    query = supabase.table("words").select("*").range(offset, offset + limit - 1)
    if level:
        query = query.eq("level", level)
    if theme:
        query = query.eq("theme", theme)
    result = query.execute()
    return {"status": "ok", "data": result.data}


@router.get("/{word_id}")
def get_word(word_id: int):
    supabase = get_supabase_client()
    result = supabase.table("words").select("*").eq("id", word_id).limit(1).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Word not found")
    return {"status": "ok", "data": result.data[0]}


@router.put("/{word_id}")
def update_word(word_id: int, payload: WordUpdate):
    supabase = get_supabase_client()
    data = payload.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = (
        supabase.table("words").update(data).eq("id", word_id).execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Word not found")
    return {"status": "ok", "data": result.data[0]}


@router.delete("/{word_id}")
def delete_word(word_id: int):
    supabase = get_supabase_client()
    result = supabase.table("words").delete().eq("id", word_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Word not found")
    return {"status": "ok", "data": result.data[0]}
