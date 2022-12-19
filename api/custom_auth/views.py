from custom_auth.serializers import TokenCreateSerializer, TokenSerializer, UserCreateSerializer
from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class TokenCreateView(generics.GenericAPIView):
    """
    Use this endpoint to obtain user authentication token.
    """

    serializer_class = TokenCreateSerializer

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, _ = Token.objects.get_or_create(user=serializer.user)
        token_serializer = TokenSerializer(token)
        return Response(
            data=token_serializer.data, status=status.HTTP_200_OK
        )
