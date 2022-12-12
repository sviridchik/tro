import datetime
import json

import matplotlib.pyplot as plt
import numpy as np
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from statistic.models import TakenMed, MissedMed

from .models import Cure, TimeTable, Schedule
from .serializers import CureSerializer, ScheduleSerializer, MainCureSerializer, \
    MainTimeTableSerializer
from managment.models import Patient


class MainView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Cure.objects.all()
    serializer_class = CureSerializer

    def get_queryset(self):
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        patient: Patient = request.user.patient
        return resp

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


class CollectStatisticView(generics.ListAPIView):
    """отчет за последни е 10 дней"""
    permission_classes = (AllowAny,)
    queryset = Cure.objects.all()
    serializer_class = CureSerializer

    def list(self, request, *args, **kwargs):
        cures = Cure.objects.filter(user=request.user.patient)
        cures_taken = TakenMed.objects.filter(user=request.user.patient)
        cures_taken = [c.id for c in cures_taken]
        today = datetime.datetime.now().date()
        today_time = datetime.datetime.now().time()
        missed_count = 0
        taken_count = 0

        for cure in cures:
            if cure.schedule.cycle_start <= today and cure.schedule.cycle_end >= today:
                tmp = {}
                tmp["cure"] = MainCureSerializer(cure).data
                if cure.id not in cures_taken:
                    missed_count += 0
                    MissedMed.objects.create(patient=request.user.patient, med=cure, date=today, is_informed=False)

                else:
                    taken_count += 1

        data = {}
        with open('data.json') as json_file:
            data = json.load(json_file)
            data["data"]["taken"].append(taken_count)
            data["data"]["missed"].append(missed_count)

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        x, y = None, None

        with open('data.json') as json_file:
            data = json.load(json_file)
            x = data["data"]["taken"]
            y = data["data"]["missed"]
        if len(x) > 10:
            x, y = x[-10:], y[-10:]
        barWidth = 0.3
        r1 = np.arange(len(x))
        r2 = [x + barWidth for x in r1]
        plt.bar(r1, x, width=barWidth, color='blue', edgecolor='black', capsize=7, label='3')

        plt.bar(r2, y, width=barWidth, color='orange', edgecolor='black', capsize=7, label='4')
        titles = ["taken", "missed"]

        plt.xticks([r + barWidth for r in range(len(x))], titles, rotation=90, fontsize=5)
        plt.ylabel('height')
        plt.subplots_adjust(bottom=0.5, top=0.99)
        plt.legend()
        plt.savefig('graf.png')

        return Response({}, status=status.HTTP_200_OK)


class TakeView(mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    queryset = Cure.objects.all()
    serializer_class = CureSerializer

    def get_queryset(self):
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GraficsView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Cure.objects.all()
    serializer_class = CureSerializer

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        with open('data.json') as json_file:
            data = json.load(json_file)
            raise Exception(data)
        x = [1, 2, 0, 4, 5, 9, 1, 0, 7, 8]
        y = [1, 1, 0, 0, 0, 2, 3, 4, 5, 0]

        barWidth = 0.3
        r1 = np.arange(len(x))
        r2 = [x + barWidth for x in r1]
        # print(list(data.keys())[1:-2], list(data.values())[1:-2])
        plt.bar(r1, x, width=barWidth, color='blue', edgecolor='black', capsize=7, label='3')

        # Create cyan bars
        plt.bar(r2, y, width=barWidth, color='orange', edgecolor='black', capsize=7, label='4')
        titles = []
        for i in range(len(x)):
            titles.append(str(i))
        # general layout
        plt.xticks([r + barWidth for r in range(len(x))], titles, rotation=90, fontsize=5)
        plt.ylabel('height')
        plt.subplots_adjust(bottom=0.5, top=0.99)

        plt.legend()

        # Show graphic
        plt.show()

        return Response({}, status=status.HTTP_200_OK)


class CureViewSet(viewsets.ModelViewSet):
    queryset = Cure.objects.all()
    serializer_class = MainCureSerializer

    # def create(self):


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = MainTimeTableSerializer
