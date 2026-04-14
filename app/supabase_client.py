from functools import lru_cache

from supabase import create_client

from app.config import get_env


@lru_cache(maxsize=1)
def get_supabase_client():
    env = get_env()
    url = env.get("SUPABASE_URL")
    key = env.get("SUPABASE_SERVICE_ROLE_KEY") or env.get("SUPABASE_ANON_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_*_KEY in .env")
    return create_client(url, key)
