import os

from dotenv import load_dotenv

load_dotenv()

REQUIRED_ENV_KEYS = [
    "SUPABASE_URL",
    "SUPABASE_ANON_KEY",
    "SUPABASE_SERVICE_ROLE_KEY",
]


def get_env():
    return {
        key: os.getenv(key)
        for key in REQUIRED_ENV_KEYS
        + ["OPENAI_API_KEY", "OPENAI_MODEL", "RATE_LIMIT_PER_MIN", "LOG_DIR", "APP_ENV", "SKIP_ENV_CHECK"]
    }


def validate_env():
    if not should_validate_env():
        return get_env()
    env = get_env()
    if not env["SUPABASE_URL"]:
        raise RuntimeError("Missing SUPABASE_URL in .env")
    if not (env["SUPABASE_SERVICE_ROLE_KEY"] or env["SUPABASE_ANON_KEY"]):
        raise RuntimeError("Missing SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY in .env")
    return env


def should_validate_env():
    return os.getenv("SKIP_ENV_CHECK") != "1" and os.getenv("APP_ENV") != "test"


def rate_limit_per_min():
    try:
        return int(os.getenv("RATE_LIMIT_PER_MIN", "120"))
    except ValueError:
        return 120


def log_dir():
    return os.getenv("LOG_DIR", "logs")
