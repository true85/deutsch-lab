from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import verify_api_key
from app.schemas.user_state import (
    UserExpressionStateCreate,
    UserExpressionStateUpdate,
    UserGrammarStateCreate,
    UserGrammarStateUpdate,
    UserScenarioStateCreate,
    UserScenarioStateUpdate,
    UserWordStateCreate,
    UserWordStateUpdate,
)
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/user-state", tags=["user-state"], dependencies=[Depends(verify_api_key)])


def _list_states(table: str, user_id: int | None, limit: int, offset: int):
    supabase = get_supabase_client()
    query = supabase.table(table).select("*").range(offset, offset + limit - 1)
    if user_id is not None:
        query = query.eq("user_id", user_id)
    result = query.execute()
    return {"status": "ok", "data": result.data}


def _get_state(table: str, state_id: int):
    supabase = get_supabase_client()
    result = supabase.table(table).select("*").eq("id", state_id).limit(1).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="State not found")
    return {"status": "ok", "data": result.data[0]}


def _create_state(table: str, payload):
    supabase = get_supabase_client()
    result = supabase.table(table).insert(payload.model_dump()).execute()
    if not result.data:
        raise HTTPException(status_code=400, detail="Failed to create state")
    return {"status": "ok", "data": result.data[0]}


def _update_state(table: str, state_id: int, payload):
    supabase = get_supabase_client()
    data = payload.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = supabase.table(table).update(data).eq("id", state_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="State not found")
    return {"status": "ok", "data": result.data[0]}


def _delete_state(table: str, state_id: int):
    supabase = get_supabase_client()
    result = supabase.table(table).delete().eq("id", state_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="State not found")
    return {"status": "ok", "data": result.data[0]}


@router.get("/words")
def list_word_states(
    user_id: int | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    return _list_states("user_word_state", user_id, limit, offset)


@router.post("/words")
def create_word_state(payload: UserWordStateCreate):
    return _create_state("user_word_state", payload)


@router.get("/words/{state_id}")
def get_word_state(state_id: int):
    return _get_state("user_word_state", state_id)


@router.put("/words/{state_id}")
def update_word_state(state_id: int, payload: UserWordStateUpdate):
    return _update_state("user_word_state", state_id, payload)


@router.delete("/words/{state_id}")
def delete_word_state(state_id: int):
    return _delete_state("user_word_state", state_id)


@router.get("/grammar")
def list_grammar_states(
    user_id: int | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    return _list_states("user_grammar_state", user_id, limit, offset)


@router.post("/grammar")
def create_grammar_state(payload: UserGrammarStateCreate):
    return _create_state("user_grammar_state", payload)


@router.get("/grammar/{state_id}")
def get_grammar_state(state_id: int):
    return _get_state("user_grammar_state", state_id)


@router.put("/grammar/{state_id}")
def update_grammar_state(state_id: int, payload: UserGrammarStateUpdate):
    return _update_state("user_grammar_state", state_id, payload)


@router.delete("/grammar/{state_id}")
def delete_grammar_state(state_id: int):
    return _delete_state("user_grammar_state", state_id)


@router.get("/expressions")
def list_expression_states(
    user_id: int | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    return _list_states("user_expression_state", user_id, limit, offset)


@router.post("/expressions")
def create_expression_state(payload: UserExpressionStateCreate):
    return _create_state("user_expression_state", payload)


@router.get("/expressions/{state_id}")
def get_expression_state(state_id: int):
    return _get_state("user_expression_state", state_id)


@router.put("/expressions/{state_id}")
def update_expression_state(state_id: int, payload: UserExpressionStateUpdate):
    return _update_state("user_expression_state", state_id, payload)


@router.delete("/expressions/{state_id}")
def delete_expression_state(state_id: int):
    return _delete_state("user_expression_state", state_id)


@router.get("/scenarios")
def list_scenario_states(
    user_id: int | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    return _list_states("user_scenario_state", user_id, limit, offset)


@router.post("/scenarios")
def create_scenario_state(payload: UserScenarioStateCreate):
    return _create_state("user_scenario_state", payload)


@router.get("/scenarios/{state_id}")
def get_scenario_state(state_id: int):
    return _get_state("user_scenario_state", state_id)


@router.put("/scenarios/{state_id}")
def update_scenario_state(state_id: int, payload: UserScenarioStateUpdate):
    return _update_state("user_scenario_state", state_id, payload)


@router.delete("/scenarios/{state_id}")
def delete_scenario_state(state_id: int):
    return _delete_state("user_scenario_state", state_id)
