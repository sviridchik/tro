import datetime
import json
import math
import numpy as np
import matplotlib.pyplot as plt
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Devise, Logs, MissedMed, TakenMed,Achievement,Label,ReportDot
from .serializers import DeviseSerializer, LogsSerializer, MissedMedSerializer, TakenMedSerializer,AchievementSerializer,LabelSerializer

class AnalyticTakenView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = TakenMed.objects.all()
    serializer_class = TakenMedSerializer

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        # TODO:to make it right
        final_data = {"принятые":0,
                      "пропущенные":0 }
        cures = TakenMed.objects.all()
        cures_missed = MissedMed.objects.all()

        date_data = request.GET.get("date_data")
        if date_data:

            date_data = date_data.split(".")

            for i in range(len(date_data)):

                if date_data[i].startswith("0"):

                    date_data[i] = date_data[i][1:]
            date_data = [eval(el) for el in date_data]
            date_data = datetime.date(date_data[-1], date_data[-2], date_data[-3])

            cures = cures.filter(date__date = date_data)
            cures_missed = cures_missed.filter(date__date = date_data)
            res = TakenMedSerializer(cures, many=True)
            res_missed = MissedMedSerializer(cures_missed, many=True)
        else:
            res  = TakenMedSerializer(cures, many=True)
            res_missed = MissedMedSerializer(cures_missed, many=True)

        final_data["принятые"] = res.data
        final_data["пропущенные"] = res_missed.data



        return Response(final_data, status=status.HTTP_200_OK)

class DeviseViewSet(viewsets.ModelViewSet):
    queryset = Devise.objects.all()
    serializer_class = DeviseSerializer


class LogsViewSet(viewsets.ModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogsSerializer

class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

class MissedMedViewSet(viewsets.ModelViewSet):
    queryset = MissedMed.objects.all()
    serializer_class = MissedMedSerializer


class TakenMedViewSet(viewsets.ModelViewSet):
    queryset = TakenMed.objects.all()
    serializer_class = TakenMedSerializer



class AnalyticTakenView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = TakenMed.objects.all()
    serializer_class = TakenMedSerializer

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        # TODO:to make it right (чтобы только для конкретного пользователя)
        report = ReportDot.objects.all()
        x = report.x
        y = report.y
        # x = [1, 2, 0, 4, 5, 9, 1, 0, 7, 8]
        # y = [1, 1, 0, 0, 0, 2, 3, 4, 5, 0]

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
