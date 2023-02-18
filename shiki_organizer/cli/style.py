colors = {
    "id": "red",
    "name": "green",
    "tags": "yellow",
    "duration": "blue",
    "days": "magenta",
    "average": "cyan",
    "parent": "red",
    "scheduled": "green",
    "recurrence": "yellow",
    "status": "blue",
    "deadline": "magenta",
    "task_id": "yellow",
    "end": "magenta",
    "start": "cyan",
}


def duration_to_str(duration, style="bold blue"):
    seconds = int(duration)
    minutes = int(duration / 60)
    hours = int(minutes / 60)
    seconds = seconds % 60
    minutes = minutes % 60
    hours = f"{hours}h " if hours else ""
    return f"[{style}]{hours}{minutes}m {seconds}s[/{style}]"
