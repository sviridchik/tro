from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs


class TokenCreateSerializer(serializers.Serializer):
    password = serializers.CharField(required=False, style={"input_type": "password"})
    username = serializers.CharField(required=False)

    def validate(self, attrs):
        password = attrs.get("password")
        self.user = authenticate(
            request=self.context.get("request"), username=attrs.get('username'), password=password
        )
        if not self.user:
            self.user = User.objects.filter(username=attrs.get('username')).first()
            if self.user and not self.user.check_password(password):
                raise ValidationError('Unable to log in with provided credentials.')
        if self.user and self.user.is_active:
            return attrs
        raise ValidationError('Unable to log in with provided credentials.')


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")

    class Meta:
        model = Token
        fields = ("auth_token",)
