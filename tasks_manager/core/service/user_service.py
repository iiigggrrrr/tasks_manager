from django.db.models import Q

from core.models import InviteForRegistration, Task, CompanyUser


def is_email_invited(email: str) -> bool:
    return InviteForRegistration.objects.filter(invited_email=email).exists()


def obtain_task_by_user(user: CompanyUser, task: Task):
    task.status = Task.Status.IN_PROGRESS
    task.performer = user
    task.save()


def finish_task(task: Task, report: str):
    task.report = report
    task.status = Task.Status.COMPLETED
    task.save()
