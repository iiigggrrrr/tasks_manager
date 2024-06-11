from rest_framework import serializers

from core.models import CompanyUser


MSG = {
    "NotFound": {"username": "user with such username not found"},
    "WrongPassword": {"password": "wrong password for this user"},
}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = CompanyUser.objects.filter().first()
        if not user:
            raise serializers.ValidationError(MSG["NotFound"], code="authorization")
        if not user.check_password(password):
            raise serializers.ValidationError(
                MSG["WrongPassword"], code="authorization"
            )

        return user.id
