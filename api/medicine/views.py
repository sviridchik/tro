import datetime

from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Cure, TimeTable, Schedule
from .serializers import CureSerializer, ScheduleSerializer, MainCureSerializer, \
    MainTimeTableSerializer


class MainView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Cure.objects.all()
    serializer_class = CureSerializer

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        # TODO:to make it right
        cures = Cure.objects.filter(user=request.user.patient)
        # cures = Cure.objects.all()

        today = datetime.datetime.now().date()
        res = []
        for cure in cures:
            if cure.schedule.cycle_start <= today and cure.schedule.cycle_end >= today:
                tmp = {}
                tmp["cure"] = MainCureSerializer(cure).data
                tmp["time"] = MainTimeTableSerializer(TimeTable.objects.filter(schedule=cure.schedule), many=True).data
                res.append(tmp)

        res = {"data": res}

        return Response(res, status=status.HTTP_200_OK)


class TimeTableView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Cure.objects.all()
    serializer_class = CureSerializer

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        # TODO:to make it right

        cures = Cure.objects.filter(user=request.user.patient)

        date_data = request.GET.get("date_data").split(".")
        for i in range(len(date_data)):
            if date_data[i].startswith("0"):
                date_data[i] = date_data[i][1:]
        # raise Exception(date_data, int(date_data[0]))
        date_data = [eval(el) for el in date_data]
        date_data = datetime.date(date_data[-1],date_data[-2],date_data[-3])
        # raise Exception(date_data)
        res = []
        t = []
        for cure in cures:
            t.append(cure.schedule.cycle_start)

            if cure.schedule.cycle_start <= date_data and cure.schedule.cycle_end >= date_data:
                tmp = {}
                tmp["cure"] = MainCureSerializer(cure).data
                tmp["time"] = MainTimeTableSerializer(TimeTable.objects.filter(schedule=cure.schedule), many=True).data
                res.append(tmp)

        # raise Exception(t[2],date_data, t[2]<=date_data)

        res = {"data": res}
        return Response(res, status=status.HTTP_200_OK)


class CureViewSet(viewsets.ModelViewSet):
    queryset = Cure.objects.all()
    serializer_class = MainCureSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = MainTimeTableSerializer
