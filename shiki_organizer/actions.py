import datetime as dt
import math
import uuid

from shiki_organizer.database import Interval, Task
from shiki_organizer.settings import Settings


def diff(a, b):
    result = ""
    flag = False
    for c_a, c_b in zip(a, b):
        if c_a != c_b:
            flag = True
        if flag:
            result += c_b
    return result


def get_status(message="Tracking") -> str:
    interval = Interval.select().order_by(Interval.start.desc()).get()
    task = interval.task
    end = interval.end if interval.end else dt.datetime.now()
    duration = str(
        dt.timedelta(seconds=math.floor((end - interval.start).total_seconds()))
    ).rjust(21, " ")
    start = interval.start.strftime("%Y-%m-%dT%H:%M:%S").rjust(19, " ")
    end = diff(start, end.strftime("%Y-%m-%dT%H:%M:%S")).rjust(19, " ")
    return f'{message} "{task.name}"\n  Started {interval.start}\n  Current {end}\n  Total {duration}'


def start(task: str, start, end):
    task = Task.get_by_id(int(task))
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        if interval.task == task:
            print(get_status())
            return
        else:
            now = dt.datetime.now()
            interval.end = dt.datetime(
                now.year, now.month, now.day, now.hour, now.minute, now.second
            )
            interval.save()
            print(get_status("Recorded"))
    if end and end < start:
        end = None
        print("The end of the interval must be after the start.")
        return
    Interval.create(task=task, start=start, end=end)
    print(get_status())


def get_current_task():
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        return interval.task


def close_issue(task: Task, github_token: str):
    issue = Issue.get_or_none(Issue.task == task)
    if issue:
        if not github_token:
            print("GitHub token is required.")
            return
        g = Github(github_token)
        repo = g.get_repo(issue.repository.name)
        open_issues = repo.get_issues(state="open")
        for i in open_issues:
            if issue.id == i.number:
                i.edit(state="closed")
        print(f"Close issue {task.id} '{task.name}'.")


def done(tasks: list):
    for task in tasks:
        task = Task.get_by_id(int(task))
        interval = Interval.get_or_none(
            (Interval.end == None) & (Interval.task == task)
        )
        if interval:
            print(get_status("Recorded"))
            interval.end = dt.datetime.now()
            interval.save()
        if task.recurrence:
            task.scheduled = (
                dt.datetime.now() + dt.timedelta(days=task.recurrence)
            ).date()
            if task.deadline and task.scheduled > task.deadline:
                task.archived = True
                task.scheduled = dt.datetime.now()
        else:
            task.archived = True
        task.save()
        if not task.archived:
            print(f"Reschedule task {task.id} '{task.name}' to {task.scheduled}.")
        else:
            print(f"Completed task {task.id} '{task.name}'.")


def stop():
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        print(get_status("Recorded"))
        now = dt.datetime.now()
        interval.end = dt.datetime(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )
        interval.save()
    else:
        print("There is no active time tracking.")


def pull():
    settings = Settings()
    message = []

    def process_issue(issues, repository, is_closed=False):
        for i in issues:
            created = False
            issue, _ = Issue.get_or_create(id=i.number, repository=repository)
            if not issue.task:
                task = Task.create(
                    description=i.title,
                )
                issue.task = task
                message.append(f"Created task '{task.name}'.")
                created = True
            task = issue.task
            old_description = task.name if task.name else None
            task.name = f"{i.title} #{issue.id}"
            if not created and old_description and task.name != old_description:
                message.append(f"Rename task '{old_description}' to '{task.name}'.")
            task.parent = repository.parent
            task.archived = is_closed
            task.save()
            issue.save()
            Task.reindex()

    if not settings.github_token:
        raise Exception("GitHub token is required")
    g = Github(settings.github_token)

    for repository in Repository.select():
        repo = g.get_repo(repository.name)
        open_issues = repo.get_issues(state="open")
        closed_issues = repo.get_issues(state="closed")
        process_issue(open_issues, repository)
        process_issue(closed_issues, repository, True)
    return "\n".join(message)
