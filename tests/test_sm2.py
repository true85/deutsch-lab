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
