from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from core.managers import CompanyUserManager


class CompanyUser(AbstractUser):
    class Roles(models.TextChoices):
        CUSTOMER = 'customer'
        EMPLOYEE = 'employee'
        ADVANCED_EMPLOYEE = 'advanced_employee'
        ADMIN = "admin"

    username = None
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    role = models.CharField(max_length=64, choices=Roles.choices)
    # some users don't have a middle name, so blank is True
    middle_name = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'middle_name', 'phone_number']

    objects = CompanyUserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Task(models.Model):
    class Status(models.IntegerChoices):
        WAITING_FOR_PERFORMER = 1, 'WAITING FOR PERFORMER'
        IN_PROGRESS = 2, 'IN PROGRESS'
        COMPLETED = 3, 'COMPLETED'
        CLOSED = 4, 'CLOSED'

    status = models.IntegerField(choices=Status.choices, default=Status.WAITING_FOR_PERFORMER)
    customer = models.ForeignKey(CompanyUser, on_delete=models.PROTECT, related_name='customer', null=False)
    performer = models.ForeignKey(CompanyUser, on_delete=models.PROTECT, related_name='performer', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    report = models.TextField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at'])
        ]


class InviteForRegistration(models.Model):
    invited_email = models.EmailField(unique=True)
    invited_by = models.ForeignKey(CompanyUser, on_delete=models.PROTECT, related_name='invited_by', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
