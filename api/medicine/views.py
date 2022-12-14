import datetime
import json

import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import get_object_or_404
from managment.models import Patient
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from statistic.models import TakenMed, MissedMed
from statistic.serializers import TakenMedSerializer

from .models import Cure, TimeTable, Schedule
from .serializers import CureSerializer, ScheduleSerializer, MainCureSerializer, \
    MainTimeTableSerializer


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


class TakeViewSet(generics.RetrieveAPIView):
    # permission_classes = (AllowAny,)
    queryset = Cure.objects.all()

    def get(self, request, pk, *args, **kwargs):
        queryset = Cure.objects.all()
        cure = get_object_or_404(queryset, pk=pk)
        today = datetime.datetime.now().date()
        today_time = datetime.datetime.now()
        today_time = today_time.replace()
        flag_is_late = True
        if cure.schedule.cycle_start <= today and cure.schedule.cycle_end >= today:
            tmp = {}
            tmp["cure"] = MainCureSerializer(cure).data
            times = MainTimeTableSerializer(TimeTable.objects.filter(schedule=cure.schedule), many=True).data

            for t in times:
                time_processed = datetime.datetime.strptime(t["time"], '%H:%M:%S')
                if not cure.strict_status:
                    if time_processed.hour == today_time.hour:
                        flag_is_late = False
                        # raise Exception(time_processed.hour ,today_time.hour)
                        break
                else:
                    if time_processed.hour == today_time.hour and time_processed.minute == today_time.minute:
                        flag_is_late = False
                        # raise Exception(time_processed.hour ,today_time.hour)
                        break

            TakenMed.objects.create(patient=request.user.patient, med=cure, date=today, report=False,
                                    is_late=flag_is_late)
            serializer = TakenMedSerializer(TakenMed.objects.last())
        else:
            return Response({"error": "no need to take it"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


class CureViewSet(viewsets.ModelViewSet):
    queryset = Cure.objects.all()
    serializer_class = MainCureSerializer

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        patient: Patient = request.user.patient
        return resp


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = MainTimeTableSerializer
