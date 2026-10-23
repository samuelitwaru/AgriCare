from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "phone_number",
            "preferred_language",
            "organization",
        ]
        read_only_fields = ["id", "role"]


class RegisterSerializer(serializers.ModelSerializer):
    """Public self-registration. Role is deliberately not settable here -
    it always defaults to farmer (the model default); extension agents,
    institution admins, and platform admins are provisioned separately
    (Django admin, or a future authenticated invite flow), never by a
    caller choosing their own role on signup.
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "phone_number",
            "preferred_language",
            "organization",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
