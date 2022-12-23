import pendulum
import datetime as dt


def period_to_datetime(period: str):
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
            start = dt.datetime.min
    if start != dt.datetime.min:
        start_string = start.to_datetime_string()
        start = dt.datetime.fromisoformat(start_string)
    return start
