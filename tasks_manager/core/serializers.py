from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import CompanyUser, Task, InviteForRegistration


class UserRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(max_length=255, write_only=True)
    middle_name = serializers.CharField(max_length=64, required=False)
    role = serializers.CharField(max_length=64, required=True)

    class Meta:
        model = CompanyUser
        fields = ('phone_number', 'email', 'first_name', 'last_name', 'middle_name', 'password', 'id', 'role')

    def is_valid(self, raise_exception=True):
        super(UserRegistrationSerializer, self).is_valid(raise_exception=raise_exception)
        if self.validated_data['role'] not in (CompanyUser.Roles.CUSTOMER, CompanyUser.Roles.EMPLOYEE):
            raise serializers.ValidationError('Invalid role')
        return True


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyUser
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'middle_name']
        read_only_fields = ('email', 'phone_number')


class CreateTaskSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    id = serializers.UUIDField(read_only=True)
    customer = UserSerializer(read_only=True)
    customer_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Task
        fields = ['id', 'status', 'customer_id', 'customer', 'performer', 'created_at',
                  'updated_at', 'completed_at', 'report']
        read_only_fields = ('id', 'created_at', 'updated_at', 'completed_at')
        depth = 1


class InviteForRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteForRegistration
        fields = ['invited_email', 'invited_by']


class UpdateTaskSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=True)
    customer = UserSerializer(read_only=True, required=False)
    performer = UserSerializer(read_only=True, required=False)
    report = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'


class FinishTaskSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=True)
    report = serializers.CharField(write_only=True)

    class Meta:
        model = Task
        fields = ['id', 'performer', 'report']

    def is_valid(self, raise_exception=True):
        super(FinishTaskSerializer, self).is_valid(raise_exception=raise_exception)
        if self.validated_data['performer'].id != Task.objects.get(id=self.validated_data['id']).performer_id:
            raise ValidationError({'id': 'You have no such task'})


class FreeTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'customer', 'created_at', 'updated_at', 'status']
        read_only_fields = ('id', 'customer', 'created_at', 'updated_at')

    def is_valid(self, *, raise_exception=False):
        super(FreeTaskSerializer, self).is_valid(raise_exception=raise_exception)


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'customer', 'created_at', 'updated_at', 'status']
        read_only_fields = ('id', 'created_at', 'updated_at')


class ObtainedTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'performer', 'customer', 'created_at', 'updated_at', 'status', 'report']
        read_only_fields = ('id', 'performer', 'customer', 'created_at', 'updated_at')

