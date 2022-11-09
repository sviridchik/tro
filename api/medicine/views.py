from rest_framework import viewsets

from .models import Cure, TimeTable, Schedule
from .serializers import CureSerializer, ScheduleSerializer, TimeTableSerializer


class CureViewSet(viewsets.ModelViewSet):
    queryset = Cure.objects.all()
    serializer_class = CureSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
