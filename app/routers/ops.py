from fastapi import APIRouter

from app.config import rate_limit_per_min
from app.llm.usage_tracker import snapshot

router = APIRouter(prefix="/ops", tags=["ops"])


@router.get("/usage")
def usage():
    return {"status": "ok", "data": snapshot()}


@router.get("/rate-limit")
def rate_limit():
    return {"status": "ok", "data": {"per_min": rate_limit_per_min()}}
