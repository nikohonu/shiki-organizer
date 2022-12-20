import datetime as dt
import math
import uuid

from github import Github
from shiki_organizer.model import Interval, Issue, Task


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
    return f'{message} "{task.description}"\n  Started {interval.start}\n  Current {end}\n  Total {duration}'


def start(task: str, start, end):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
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
    Interval.reindex()


def get_current_task():
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        return interval.task


def done(tasks: list, github_token):
    for task in tasks:
        if task.isnumeric():
            task = Task.get_by_id(int(task))
        else:
            task = Task.get_by_uuid(uuid.UUID(task))
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
        print(f"Completed task {task.id} '{task.description}'.")
        if not task.archived:
            print(
                f"Reschedule task {task.id} '{task.description}' to {task.scheduled}."
            )
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
            print(f"Close issue {task.id} '{task.description}'.")


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
