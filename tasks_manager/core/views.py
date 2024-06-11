from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, OR, AND
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Task, CompanyUser
from core.permissions import IsCustomer, IsEmployee, IsAdvancedEmployee
from core.serializers import UserSerializer, UserRegistrationSerializer, CreateTaskSerializer, \
    InviteForRegistrationSerializer, FreeTaskSerializer, TaskSerializer, \
    ObtainedTaskSerializer
from core.service import user_service
from core.service.user_service import is_email_invited


class RegistrationAPIView(APIView):

    def post(self, request) -> Response:
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not is_email_invited(serializer.validated_data['email']):
            return Response(data={'msg': 'You should be invited by another user'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(data={'msg': 'success'}, status=status.HTTP_201_CREATED)


class CreateTaskAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request):
        request.data.setdefault('customer_id', request.user.id)
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class FreeTaskViewSet(ModelViewSet):
    queryset = Task.objects.filter(status=Task.Status.WAITING_FOR_PERFORMER)
    serializer_class = FreeTaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployee]

    @action(detail=True, methods=['get'], url_path='obtain')
    def obtain_task(self, request, *args, **kwargs):
        user_service.obtain_task_by_user(request.user, self.get_object())
        return Response(data={'msg': 'success'}, status=status.HTTP_200_OK)


class CustomerTaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [
        AND(
            IsAuthenticated,
            OR(
                IsCustomer,
                IsAdvancedEmployee
            )
        )
    ]
    permission_classes_per_method = {
        'create': [IsAuthenticated, (IsCustomer | IsAdvancedEmployee)],
    }

    def get_permissions(self):
        try:
            # Return the set of permissions based on the incoming request method
            return [permission() for permission in self.permission_classes_per_method[self.action]]
        except KeyError:
            # Default to the standard set of permissions
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.setdefault('customer', request.user.id)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def get_queryset(self):
        customer = self.request.user
        customer_tasks = Task.objects.filter(customer_id=customer.id)
        return customer_tasks

    @action(detail=True, methods=['post'])
    def close(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = Task.Status.CLOSED
        task.save()
        return Response(status=status.HTTP_200_OK)


class InviteUserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployee]

    def post(self, request):
        data = request.data.copy()
        data['invited_by'] = request.user.id
        serializer = InviteForRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'msg': 'success'}, status=status.HTTP_201_CREATED)


class PerformerTaskViewSet(ModelViewSet):
    serializer_class = ObtainedTaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployee]

    def get_queryset(self):
        employee = self.request.user
        employee_obtained_tasks = Task.objects.filter(performer_id=employee.id)
        return employee_obtained_tasks

    @action(detail=True, methods=['post'])
    def finish(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_service.finish_task(
            self.get_object(),
            serializer.validated_data['report']
        )
        return Response(data={'msg': 'success'}, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCustomer]
    queryset = CompanyUser.objects.all()
