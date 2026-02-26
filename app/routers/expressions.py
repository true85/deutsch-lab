from fastapi import APIRouter, HTTPException, Query

from app.schemas.expressions import ExpressionCreate, ExpressionUpdate
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/expressions", tags=["expressions"])


@router.post("")
def create_expression(payload: ExpressionCreate):
    supabase = get_supabase_client()
    result = supabase.table("expressions").insert(payload.model_dump()).execute()
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to create expression")
    return {"status": "ok", "data": result.data[0]}


@router.get("")
def list_expressions(
    level: str | None = Query(default=None),
    type: str | None = Query(default=None),
    situation: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    supabase = get_supabase_client()
    query = supabase.table("expressions").select("*").range(offset, offset + limit - 1)
    if level:
        query = query.eq("level", level)
    if type:
        query = query.eq("type", type)
    if situation:
        query = query.eq("situation", situation)
    result = query.execute()
    return {"status": "ok", "data": result.data}


@router.get("/{expression_id}")
def get_expression(expression_id: int):
    supabase = get_supabase_client()
    result = supabase.table("expressions").select("*").eq("id", expression_id).limit(1).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Expression not found")
    return {"status": "ok", "data": result.data[0]}


@router.put("/{expression_id}")
def update_expression(expression_id: int, payload: ExpressionUpdate):
    supabase = get_supabase_client()
    data = payload.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = supabase.table("expressions").update(data).eq("id", expression_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Expression not found")
    return {"status": "ok", "data": result.data[0]}


@router.delete("/{expression_id}")
def delete_expression(expression_id: int):
    supabase = get_supabase_client()
    result = supabase.table("expressions").delete().eq("id", expression_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Expression not found")
    return {"status": "ok", "data": result.data[0]}
