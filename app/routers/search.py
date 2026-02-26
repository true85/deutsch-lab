from fastapi import APIRouter, HTTPException, Query

from app.llm.openai_client import get_embedding
from app.supabase_client import get_supabase_client

router = APIRouter(prefix="/search", tags=["search"])


def _rpc_vector_search(fn_name: str, embedding: list[float], limit: int):
    supabase = get_supabase_client()
    result = supabase.rpc(
        fn_name,
        {
            "query_embedding": embedding,
            "match_count": limit,
        },
    ).execute()
    if result.data is None:
        raise HTTPException(status_code=500, detail=f"RPC {fn_name} failed")
    return {"status": "ok", "data": result.data}


@router.get("/words")
def search_words(q: str = Query(...), limit: int = Query(20, ge=1, le=100)):
    return _rpc_vector_search("match_words", get_embedding(q), limit)


@router.get("/grammar")
def search_grammar(q: str = Query(...), limit: int = Query(20, ge=1, le=100)):
    return _rpc_vector_search("match_grammar", get_embedding(q), limit)


@router.get("/expressions")
def search_expressions(q: str = Query(...), limit: int = Query(20, ge=1, le=100)):
    return _rpc_vector_search("match_expressions", get_embedding(q), limit)


@router.get("/scenarios")
def search_scenarios(q: str = Query(...), limit: int = Query(20, ge=1, le=100)):
    return _rpc_vector_search("match_scenarios", get_embedding(q), limit)
