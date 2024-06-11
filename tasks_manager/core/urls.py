from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import RegistrationAPIView, CreateTaskAPIView, \
    InviteUserAPIView, FreeTaskViewSet, CustomerTaskViewSet, PerformerTaskViewSet, UserViewSet

free_tasks_router = DefaultRouter()
free_tasks_router.register(r'tasks', FreeTaskViewSet, basename='task')

customer_router = DefaultRouter()
customer_router.register(r'tasks', CustomerTaskViewSet, basename='my_task')

employee_router = DefaultRouter()
employee_router.register(r'tasks', PerformerTaskViewSet, basename='my_task')

user_router = DefaultRouter()
user_router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('user/register/', RegistrationAPIView.as_view()),
    path('task/create/', CreateTaskAPIView.as_view()),
    path('', include(free_tasks_router.urls)),
    path('employee/', include(employee_router.urls)),
    path('customer/', include(customer_router.urls)),
    path('user/invite/', InviteUserAPIView.as_view()),
    path('', include(user_router.urls))
]
