from fastapi import APIRouter, HTTPException, Query

from app.schemas.grammar import GrammarCreate, GrammarUpdate
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/grammar", tags=["grammar"])


@router.post("")
def create_grammar(payload: GrammarCreate):
    supabase = get_supabase_client()
    result = supabase.table("grammar").insert(payload.model_dump()).execute()
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to create grammar")
    return {"status": "ok", "data": result.data[0]}


@router.get("")
def list_grammar(
    level: str | None = Query(default=None),
    category: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    supabase = get_supabase_client()
    query = supabase.table("grammar").select("*").range(offset, offset + limit - 1)
    if level:
        query = query.eq("level", level)
    if category:
        query = query.eq("category", category)
    result = query.execute()
    return {"status": "ok", "data": result.data}


@router.get("/{grammar_id}")
def get_grammar(grammar_id: int):
    supabase = get_supabase_client()
    result = supabase.table("grammar").select("*").eq("id", grammar_id).limit(1).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Grammar not found")
    return {"status": "ok", "data": result.data[0]}


@router.put("/{grammar_id}")
def update_grammar(grammar_id: int, payload: GrammarUpdate):
    supabase = get_supabase_client()
    data = payload.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = supabase.table("grammar").update(data).eq("id", grammar_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Grammar not found")
    return {"status": "ok", "data": result.data[0]}


@router.delete("/{grammar_id}")
def delete_grammar(grammar_id: int):
    supabase = get_supabase_client()
    result = supabase.table("grammar").delete().eq("id", grammar_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Grammar not found")
    return {"status": "ok", "data": result.data[0]}
