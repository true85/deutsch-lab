from datetime import date, timedelta


def sm2_schedule(
    quality: int,
    reps: int,
    interval_days: int,
    ease_factor: float,
) -> dict:
    if quality < 0 or quality > 5:
        raise ValueError("quality must be 0..5")
    if quality < 3:
        reps = 0
        interval_days = 1
    else:
        reps += 1
        if reps == 1:
            interval_days = 1
        elif reps == 2:
            interval_days = 3
        else:
            interval_days = int(round(interval_days * ease_factor))
    ease_factor = max(1.3, ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
    next_review = date.today() + timedelta(days=interval_days)
    return {
        "reps": reps,
        "interval_days": interval_days,
        "ease_factor": round(ease_factor, 4),
        "next_review": next_review.isoformat(),
    }
