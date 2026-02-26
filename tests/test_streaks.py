from datetime import date, timedelta

from app.services.streaks import compute_streaks


def _iso(d: date) -> str:
    return d.isoformat() + "T00:00:00Z"


today = date.today()


def test_empty_returns_zero():
    assert compute_streaks([]) == {"current": 0, "longest": 0}


def test_single_today_streak():
    result = compute_streaks([_iso(today)])
    assert result["current"] == 1
    assert result["longest"] == 1


def test_no_today_current_zero():
    yesterday = today - timedelta(days=1)
    result = compute_streaks([_iso(yesterday)])
    assert result["current"] == 0
    assert result["longest"] == 1


def test_consecutive_days_streak():
    dates = [_iso(today - timedelta(days=i)) for i in range(5)]
    result = compute_streaks(dates)
    assert result["current"] == 5
    assert result["longest"] == 5


def test_longest_streak_in_past():
    past_start = today - timedelta(days=30)
    long_streak = [_iso(past_start + timedelta(days=i)) for i in range(7)]
    recent = [_iso(today)]
    result = compute_streaks(long_streak + recent)
    assert result["longest"] == 7
    assert result["current"] == 1


def test_duplicate_dates_counted_once():
    result = compute_streaks([_iso(today), _iso(today), _iso(today)])
    assert result["current"] == 1
    assert result["longest"] == 1
