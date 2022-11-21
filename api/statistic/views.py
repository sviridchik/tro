from rest_framework import viewsets

from .models import Devise, Logs, MissedMed, TakenMed
from .serializers import DeviseSerializer, LogsSerializer, MissedMedSerializer, TakenMedSerializer


class DeviseViewSet(viewsets.ModelViewSet):
    queryset = Devise.objects.all()
    serializer_class = DeviseSerializer


class LogsViewSet(viewsets.ModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogsSerializer


class MissedMedViewSet(viewsets.ModelViewSet):
    queryset = MissedMed.objects.all()
    serializer_class = MissedMedSerializer


class TakenMedViewSet(viewsets.ModelViewSet):
    queryset = TakenMed.objects.all()
    serializer_class = TakenMedSerializer
