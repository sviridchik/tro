# from db.datatypes import Token, User
from db import auth
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


def authenticate(username, password):
    """
    If the given credentials are valid, return a User object.
    """
    try:
        res = auth.get_user_id_by_username_and_password(username, password)
    except:
        return False
    else:
        return res


class TokenCreateSerializer(serializers.Serializer):
    password = serializers.CharField(required=False, style={"input_type": "password"})
    username = serializers.CharField(required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get("password")
        self.user_id = authenticate(username=username, password=password)
        if self.user_id:
            return attrs
        else:
            raise ValidationError('Unable to log in with provided credentials.')


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")

    class Meta:
        model = Token
        fields = ("auth_token",)
