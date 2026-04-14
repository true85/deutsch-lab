import pytest

from app.services.sm2 import sm2_schedule


def test_sm2_resets_on_fail():
    result = sm2_schedule(quality=2, reps=3, interval_days=15, ease_factor=2.5)
    assert result["reps"] == 0
    assert result["interval_days"] == 1


def test_sm2_progress_on_success():
    result = sm2_schedule(quality=4, reps=1, interval_days=3, ease_factor=2.5)
    assert result["reps"] == 2
    assert result["interval_days"] == 3
    assert result["ease_factor"] >= 1.3


@pytest.mark.parametrize("quality", [0, 1, 2])
def test_sm2_fail_quality_resets_reps_regardless(quality):
    r = sm2_schedule(quality=quality, reps=5, interval_days=30, ease_factor=2.7)
    assert r["reps"] == 0
    assert r["interval_days"] == 1


def test_sm2_quality_3_boundary_is_success():
    """quality=3은 성공 최하단 — reps 증가, ease_factor 감소."""
    r = sm2_schedule(quality=3, reps=2, interval_days=3, ease_factor=2.5)
    assert r["reps"] == 3
    assert r["ease_factor"] < 2.5  # quality<5는 ease_factor 감소


def test_sm2_reps_2_yields_interval_3():
    """최근 정책 변경: reps==2 → 6일이 아니라 3일."""
    r = sm2_schedule(quality=5, reps=1, interval_days=1, ease_factor=2.7)
    assert r["reps"] == 2
    assert r["interval_days"] == 3


def test_sm2_interval_grows_by_ease_factor_after_reps_3():
    r = sm2_schedule(quality=5, reps=2, interval_days=3, ease_factor=2.7)
    assert r["reps"] == 3
    assert r["interval_days"] == round(3 * 2.7)  # ≈ 8


def test_sm2_ease_factor_lower_bound_is_1_3():
    """연속 quality=0은 ease_factor를 1.3으로 고정."""
    r = sm2_schedule(quality=0, reps=1, interval_days=1, ease_factor=1.3)
    assert r["ease_factor"] == 1.3


@pytest.mark.parametrize("quality,exp_direction", [(3, "down"), (4, "flat"), (5, "up")])
def test_sm2_ease_factor_direction(quality, exp_direction):
    """SM-2 공식: quality=4는 EF 불변, 5는 증가, 3은 감소."""
    start = 2.5
    r = sm2_schedule(quality=quality, reps=1, interval_days=3, ease_factor=start)
    if exp_direction == "up":
        assert r["ease_factor"] > start
    elif exp_direction == "flat":
        assert r["ease_factor"] == start
    else:
        assert r["ease_factor"] < start


def test_sm2_invalid_quality_raises():
    with pytest.raises(ValueError):
        sm2_schedule(quality=6, reps=1, interval_days=1, ease_factor=2.5)
    with pytest.raises(ValueError):
        sm2_schedule(quality=-1, reps=1, interval_days=1, ease_factor=2.5)
