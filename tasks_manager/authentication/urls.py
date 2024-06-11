from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import AuthenticationAPIView

urlpatterns = [
    path('login/', AuthenticationAPIView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
