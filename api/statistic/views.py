import datetime

from managment.models import Guardian
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Devise, Logs, MissedMed, TakenMed, Achievement, Label
from .serializers import DeviseSerializer, LogsSerializer, MissedMedSerializer, TakenMedSerializer, \
    AchievementSerializer, LabelSerializer


class AnalyticTakenGuardianView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = TakenMed.objects.all()
    serializer_class = TakenMedSerializer

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        # TODO:to make it right
        user = request.user
        # user = User.objects.filter(username="ivan")[0]
        final_data = {"принятые": 0,
                      "пропущенные": 0}
        if len(Guardian.objects.filter(user=user)) == 0:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        guard = Guardian.objects.filter(user=user)[0]
        patient_care_about = guard.care_about
        cures = TakenMed.objects.filter(patient=patient_care_about)
        cures_missed = MissedMed.objects.filter(patient=patient_care_about)
        date_data = request.GET.get("date_data")
        if date_data:
            date_data = date_data.split(".")
            for i in range(len(date_data)):
                if date_data[i].startswith("0"):
                    date_data[i] = date_data[i][1:]
            date_data = [eval(el) for el in date_data]
            date_data = datetime.date(date_data[-1], date_data[-2], date_data[-3])
            cures = cures.filter(date__date=date_data)
            cures_missed = cures_missed.filter(date__date=date_data)
            res = TakenMedSerializer(cures, many=True)
            res_missed = MissedMedSerializer(cures_missed, many=True)
        else:
            date_data = datetime.datetime.now()
            cures = cures.filter(date__date=date_data)
            cures_missed = cures_missed.filter(date__date=date_data)
            res = TakenMedSerializer(cures, many=True)
            res_missed = MissedMedSerializer(cures_missed, many=True)
        final_data["принятые"] = res.data
        final_data["пропущенные"] = res_missed.data
        return Response(final_data, status=status.HTTP_200_OK)


class AnalyticTakenView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = TakenMed.objects.all()
    serializer_class = TakenMedSerializer

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        # TODO:to make it right
        final_data = {"принятые": 0,
                      "пропущенные": 0}
        # guardin
        cures = TakenMed.objects.filter(user=request.user.patient)
        cures_missed = MissedMed.objects.filter(user=request.user.patient)

        date_data = request.GET.get("date_data")
        if date_data:

            date_data = date_data.split(".")

            for i in range(len(date_data)):

                if date_data[i].startswith("0"):
                    date_data[i] = date_data[i][1:]
            date_data = [eval(el) for el in date_data]
            date_data = datetime.date(date_data[-1], date_data[-2], date_data[-3])

            cures = cures.filter(date__date=date_data)
            cures_missed = cures_missed.filter(date__date=date_data)
            res = TakenMedSerializer(cures, many=True)
            res_missed = MissedMedSerializer(cures_missed, many=True)
        else:
            res = TakenMedSerializer(cures, many=True)
            res_missed = MissedMedSerializer(cures_missed, many=True)

        final_data["принятые"] = res.data
        final_data["пропущенные"] = res_missed.data
        return Response(final_data, status=status.HTTP_200_OK)


class DeviseViewSet(viewsets.ModelViewSet):
    queryset = Devise.objects.all()
    serializer_class = DeviseSerializer
    # permission_classes = (IsAuthenticated,)


class LogsViewSet(viewsets.ModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogsSerializer
    # permission_classes = (IsAuthenticated,)


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    # permission_classes = (IsAuthenticated,)


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    # permission_classes = (IsAuthenticated,)


class MissedMedViewSet(viewsets.ModelViewSet):
    queryset = MissedMed.objects.all()
    serializer_class = MissedMedSerializer
    # permission_classes = (IsAuthenticated,)


class TakenMedViewSet(viewsets.ModelViewSet):
    queryset = TakenMed.objects.all()
    serializer_class = TakenMedSerializer
    # permission_classes = (IsAuthenticated,)
