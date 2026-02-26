import threading
import time
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 120, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        self._requests = defaultdict(deque)
        self._allow_paths = {
            "/health",
            "/supabase-health",
            "/openapi.json",
            "/docs",
            "/redoc",
        }

    async def dispatch(self, request, call_next):
        if request.url.path in self._allow_paths:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        with self._lock:
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
