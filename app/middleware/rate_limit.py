import threading
import time
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


def _extract_client_ip(request) -> str:
    # 프록시 뒤에 있을 때 X-Forwarded-For 우선 (좌측 = 최초 클라이언트)
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "unknown"


class RateLimitMiddleware(BaseHTTPMiddleware):
    _GC_INTERVAL = 300  # 5분마다 stale IP 정리

    def __init__(self, app, max_requests: int = 120, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        self._requests: dict[str, deque] = defaultdict(deque)
        self._last_gc = time.time()
        self._allow_paths = {
            "/health",
            "/supabase-health",
            "/openapi.json",
            "/docs",
            "/redoc",
        }

    def _gc_stale(self, now: float) -> None:
        if now - self._last_gc < self._GC_INTERVAL:
            return
        cutoff = now - self.window_seconds
        dead = [ip for ip, q in self._requests.items() if not q or q[-1] <= cutoff]
        for ip in dead:
            self._requests.pop(ip, None)
        self._last_gc = now

    async def dispatch(self, request, call_next):
        if request.url.path in self._allow_paths:
            return await call_next(request)

        client_ip = _extract_client_ip(request)
        now = time.time()
        with self._lock:
            self._gc_stale(now)
            q = self._requests[client_ip]
            while q and q[0] <= now - self.window_seconds:
                q.popleft()
            if len(q) >= self.max_requests:
                return JSONResponse(
                    status_code=429,
                    content={"status": "error", "detail": "rate limit exceeded"},
                )
            q.append(now)

        return await call_next(request)
