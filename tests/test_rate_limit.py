"""rate_limit 미들웨어 단위 테스트 (XFF 우선, GC, 화이트리스트)."""
from unittest.mock import MagicMock

import pytest

from app.middleware.rate_limit import RateLimitMiddleware, _extract_client_ip


def _make_request(headers=None, client_host="10.0.0.1"):
    req = MagicMock()
    req.headers = headers or {}
    req.client.host = client_host
    return req


def test_extract_client_ip_prefers_xff():
    req = _make_request({"x-forwarded-for": "1.2.3.4, 5.6.7.8"}, "10.0.0.1")
    assert _extract_client_ip(req) == "1.2.3.4"


def test_extract_client_ip_xff_trims_whitespace():
    req = _make_request({"x-forwarded-for": "  9.9.9.9  "})
    assert _extract_client_ip(req) == "9.9.9.9"


def test_extract_client_ip_uses_x_real_ip_when_no_xff():
    req = _make_request({"x-real-ip": "8.8.8.8"}, "10.0.0.1")
    assert _extract_client_ip(req) == "8.8.8.8"


def test_extract_client_ip_falls_back_to_client_host():
    req = _make_request({}, "10.0.0.99")
    assert _extract_client_ip(req) == "10.0.0.99"


def test_extract_client_ip_unknown_when_no_client():
    req = MagicMock()
    req.headers = {}
    req.client = None
    assert _extract_client_ip(req) == "unknown"


def test_gc_stale_clears_inactive_ips():
    mw = RateLimitMiddleware(app=None, max_requests=10, window_seconds=60)
    from collections import deque
    # 활성 IP: 최근 요청
    now = 1000.0
    mw._requests["active"] = deque([now - 5])
    # 비활성 IP: window 밖
    mw._requests["stale"] = deque([now - 1000])
    # 빈 큐
    mw._requests["empty"] = deque()
    mw._last_gc = 0  # GC 강제

    mw._gc_stale(now)

    assert "active" in mw._requests
    assert "stale" not in mw._requests
    assert "empty" not in mw._requests


def test_gc_stale_respects_interval():
    mw = RateLimitMiddleware(app=None)
    from collections import deque
    mw._requests["stale"] = deque([0])  # 아주 오래된 요청
    mw._last_gc = 999.0  # 방금 GC 함

    mw._gc_stale(1000.0)  # interval(300) 미경과

    assert "stale" in mw._requests  # GC 스킵


def test_allow_paths_bypass_ratelimit_config():
    mw = RateLimitMiddleware(app=None)
    assert "/health" in mw._allow_paths
    assert "/supabase-health" in mw._allow_paths
    assert "/docs" in mw._allow_paths
