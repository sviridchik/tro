import binascii
import os

from custom_auth.serializers import TokenCreateSerializer, TokenSerializer
from db import auth
from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateUserView(APIView):

    def post(self, request):
        try:
            res = auth.create_user(**request.data)
        except Exception as exc:
            return Response(str(exc), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'id': res}, status=status.HTTP_201_CREATED)


class TokenCreateView(generics.GenericAPIView):
    """
    Use this endpoint to obtain user authentication token.
    """

    serializer_class = TokenCreateSerializer

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = auth.get_token(serializer.user_id)
        if not token:
            token_key = binascii.hexlify(os.urandom(20)).decode()
            token = auth.create_token(serializer.user_id, token_key)
        token, _ = Token.objects.get_or_create(user=serializer.user_id)
        token_serializer = TokenSerializer(token)
        return Response(
            data=token_serializer.data, status=status.HTTP_200_OK
        )
