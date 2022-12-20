import datetime
import json

import matplotlib.pyplot as plt
import numpy as np
from db.medicine import create_time, delete_time, get_time, list_times, update_time, get_schedule, list_schedules, delete_schedule, update_schedule, create_schedule
from django.shortcuts import get_object_or_404
from django.utils import timezone
from managment.models import Patient
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from statistic.models import MissedMed, TakenMed
from statistic.serializers import TakenMedSerializer

from .models import Cure, Schedule, TimeTable
from .serializers import (CureSerializer, MainCureSerializer, MainScheduleSerializer, MainTimeTableSerializer,
                          ViewOnlyCureSerializer)


class CollectStatisticView(generics.ListAPIView):
    """отчет за последни е 10 дней"""
    # permission_classes = (IsAuthenticated,)
    queryset = Cure.objects.all()
    serializer_class = CureSerializer

    def list(self, request, *args, **kwargs):
        cures = Cure.objects.filter(user=request.user.patient.id)
        cures_taken = TakenMed.objects.filter(user=request.user.patient.id)
        cures_taken = [c.id for c in cures_taken]
        today = datetime.datetime.now().astimezone(timezone.get_current_timezone()).date()
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
        # TODO:
        data = {}
        with open('data.json') as json_file:
            data = json.load(json_file)
            data["data"]["taken"].append(taken_count)
            data["data"]["missed"].append(missed_count)

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        x, y = None, None

        with open('data.json') as json_file:
            # raise Exception(json.load(json_file))
            data = json.load(json_file)
            x = data["data"]["taken"]
            y = data["data"]["missed"]
        # if len(x) > 10:
        #     x, y = x[-10:], y[-10:]
        # barWidth = 0.3
        # r1 = np.arange(len(x))
        # r2 = [x + barWidth for x in r1]
        # plt.bar(r1, x, width=barWidth, color='blue', edgecolor='black', capsize=7, label='3')
        #
        # plt.bar(r2, y, width=barWidth, color='orange', edgecolor='black', capsize=7, label='4')
        # titles = ["taken", "missed"]
        #
        # plt.xticks([r + barWidth for r in range(len(x))], titles, rotation=90, fontsize=5)
        # plt.ylabel('height')
        # plt.subplots_adjust(bottom=0.5, top=0.99)
        # plt.legend()
        # plt.savefig('graf.png')

        return Response({}, status=status.HTTP_200_OK)


class TakeViewSet(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        queryset = Cure.objects.filter(patient__user=request.user.id)
        cure = get_object_or_404(queryset, pk=pk)
        today = datetime.datetime.now().astimezone(timezone.get_current_timezone()).date()
        today_time = datetime.datetime.now().astimezone(timezone.get_current_timezone())
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

            taken_med = TakenMed.objects.create(patient=request.user.patient, med=cure, date=today_time, report=False,
                                                is_late=flag_is_late)
            serializer = TakenMedSerializer(taken_med)
        else:
            return Response({"error": "no need to take it"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


class CureViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ViewOnlyCureSerializer
        else:
            return MainCureSerializer

    def get_queryset(self):
        return Cure.objects.filter(patient__user=self.request.user.id)


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = MainScheduleSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        doc = create_schedule(request.data)
        return Response({'id': doc.id})

    def update(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        update_schedule(request.user.patient.id, pk, request.data)
        return Response('OK')

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        delete_schedule(request.user.patient.id, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        model = get_schedule(request.user.patient.id, pk)
        serializer = self.get_serializer(model)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        models = list_schedules(request.user.patient.id)
        serializer = self.get_serializer(models, many=True)
        return Response(serializer.data)


class TimeTableViewSet(viewsets.ModelViewSet):
    serializer_class = MainTimeTableSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        doc = create_time(request.data)
        return Response({'id': doc.id})

    def update(self, request, *args, **kwargs):
        visit_pk = self.kwargs['pk']
        update_time(request.user.patient.id, visit_pk, request.data)
        return Response('OK')

    def destroy(self, request, *args, **kwargs):
        visit_pk = self.kwargs['pk']
        delete_time(request.user.patient.id, visit_pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        visit_pk = self.kwargs['pk']
        visit = get_time(request.user.patient.id, visit_pk)
        serializer = self.get_serializer(visit)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        visits = list_times(request.user.patient.id)
        serializer = self.get_serializer(visits, many=True)
        return Response(serializer.data)
