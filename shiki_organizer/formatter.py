import datetime as dt


def duration_to_str(duration):
    seconds = int(duration)
    minutes = int(duration / 60)
    hours = int(minutes / 60)
    seconds = seconds % 60
    minutes = minutes % 60
    hours = f"{hours}h " if hours else ""
    return f"{hours}{minutes}m {seconds}s"

def datetime_to_str(datetime: dt.datetime):
    return datetime.isoformat(" ", "seconds")