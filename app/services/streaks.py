from datetime import date, datetime, timedelta


def _parse_date(value: str) -> date:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).date()


def compute_streaks(timestamps: list[str]):
    if not timestamps:
        return {"current": 0, "longest": 0}
    dates = sorted({_parse_date(ts) for ts in timestamps})
    if not dates:
        return {"current": 0, "longest": 0}

    today = date.today()
    current = 0
    day = today
    date_set = set(dates)
    while day in date_set:
        current += 1
        day -= timedelta(days=1)

    longest = 0
    streak = 0
    prev = None
    for d in dates:
        if prev is None or d == prev + timedelta(days=1):
            streak += 1
        else:
            longest = max(longest, streak)
            streak = 1
        prev = d
    longest = max(longest, streak)
    return {"current": current, "longest": longest}
