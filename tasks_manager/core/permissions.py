from rest_framework import permissions

from core.models import CompanyUser


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user and user.role == CompanyUser.Roles.EMPLOYEE


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user and user.role == CompanyUser.Roles.CUSTOMER


class IsAdvancedEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user and user.role == CompanyUser.Roles.ADVANCED_EMPLOYEE
