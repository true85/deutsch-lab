"""80/20 추천 로직 단위 테스트 (Supabase 없이 순수 로직 검증)."""
from collections import defaultdict


def _filter_candidates(
    known_counts: dict,
    total_counts: dict,
    min_ratio: float,
    include_known_only: bool,
    limit: int,
) -> list[tuple]:
    """recommend.py의 추천 필터링 로직 추출."""
    candidates = []
    for expr_id, known_count in known_counts.items():
        total = total_counts.get(expr_id, 0)
        if total == 0:
            continue
        ratio = known_count / total
        if ratio >= min_ratio and (include_known_only or ratio < 1.0):
            candidates.append((expr_id, ratio))
    candidates.sort(key=lambda x: (-x[1], x[0]))
    return candidates[:limit]


def test_filter_basic_80_percent():
    # 표현 1: 단어 4개 중 4개 알아서 ratio=1.0 → 제외 (include_known_only=False)
    # 표현 2: 단어 5개 중 4개 알아서 ratio=0.8 → 포함
    # 표현 3: 단어 10개 중 5개 알아서 ratio=0.5 → 제외 (< min_ratio=0.8)
    known_counts = {1: 4, 2: 4, 3: 5}
    total_counts = {1: 4, 2: 5, 3: 10}
    result = _filter_candidates(known_counts, total_counts, min_ratio=0.8, include_known_only=False, limit=10)
    ids = [r[0] for r in result]
    assert 2 in ids
    assert 1 not in ids
    assert 3 not in ids


def test_filter_include_known_only():
    # include_known_only=True이면 ratio=1.0도 포함
    known_counts = {1: 4, 2: 4}
    total_counts = {1: 4, 2: 5}
    result = _filter_candidates(known_counts, total_counts, min_ratio=0.8, include_known_only=True, limit=10)
    ids = [r[0] for r in result]
    assert 1 in ids
    assert 2 in ids


def test_filter_sorted_by_ratio_desc():
    known_counts = {1: 8, 2: 9, 3: 10}
    total_counts = {1: 10, 2: 10, 3: 10}
    # ratios: 1→0.8, 2→0.9, 3→1.0 (제외)
    result = _filter_candidates(known_counts, total_counts, min_ratio=0.8, include_known_only=False, limit=10)
    assert result[0][0] == 2  # ratio 0.9 먼저
    assert result[1][0] == 1  # ratio 0.8 다음


def test_filter_limit():
    known_counts = {i: 9 for i in range(10)}
    total_counts = {i: 10 for i in range(10)}
    result = _filter_candidates(known_counts, total_counts, min_ratio=0.8, include_known_only=False, limit=3)
    assert len(result) == 3


def test_filter_zero_total_skipped():
    known_counts = {1: 5, 2: 3}
    total_counts = {1: 0, 2: 5}
    result = _filter_candidates(known_counts, total_counts, min_ratio=0.5, include_known_only=True, limit=10)
    ids = [r[0] for r in result]
    assert 1 not in ids


def test_weak_grammar_sort():
    """취약 문법 정렬 로직 검증."""
    states = [
        {"grammar_id": 1, "success_count": 8, "fail_count": 2},
        {"grammar_id": 2, "success_count": 1, "fail_count": 9},
        {"grammar_id": 3, "success_count": 5, "fail_count": 5},
    ]
    scored = []
    for row in states:
        total = row["success_count"] + row["fail_count"]
        rate = row["success_count"] / total if total else 0.0
        scored.append((row["grammar_id"], rate))
    scored.sort(key=lambda x: x[1])
    ids = [gid for gid, _ in scored]
    assert ids[0] == 2  # 성공률 0.1 (최하위)
    assert ids[-1] == 1  # 성공률 0.8 (최상위)
