import datetime as dt

import pendulum


def period_to_datetime(period: str, min_start):
    start = pendulum.now()
    match period.lower():
        case "today":
            start = start.start_of("day")
        case "week":
            start = start.start_of("week")
        case "month":
            start = start.start_of("month")
        case "year":
            start = start.start_of("year")
        case _:
            start = min_start
    if start != min_start:
        start_string = start.to_datetime_string()
        start = dt.datetime.fromisoformat(start_string)
    return start
