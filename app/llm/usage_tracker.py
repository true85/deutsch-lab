import threading


_lock = threading.Lock()
_usage = {
    "calls": 0,
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0,
    "models": {},
}


def record_usage(model: str, usage):
    with _lock:
        _usage["calls"] += 1
        _usage["prompt_tokens"] += getattr(usage, "prompt_tokens", 0) or 0
        _usage["completion_tokens"] += getattr(usage, "completion_tokens", 0) or 0
        _usage["total_tokens"] += getattr(usage, "total_tokens", 0) or 0
        _usage["models"][model] = _usage["models"].get(model, 0) + 1


def snapshot():
    with _lock:
        return dict(_usage)


def reset():
    with _lock:
        _usage.update(
            {
                "calls": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "models": {},
            }
        )
