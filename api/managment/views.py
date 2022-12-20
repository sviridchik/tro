from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Doctor, DoctorVisit, Guardian, Patient, PatientSetting, Tariff, Tokens, Tranzaction
from .serializers import (DoctorSerializer, DoctorVisitSerializer, GuardianSerializer, PatientSerializer,
                          PatientSettingSerializer, ReadOnlyDoctorVisitSerializer, TariffSerializer, TokensSerializer,
                          TranzactionSerializer, UserSerializer)
from db.managment import filter_patient_by_user, filter_guardian_by_user, get_doctor, list_doctors, delete_doctor, update_doctor, create_doctor


class WhoIAmView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        patient = filter_patient_by_user(user.id)
        guardian = filter_guardian_by_user(user.id)
        res = {"type": None,
               "user": None}
        if len(patient) != 0:
            res["type"] = "patient"
            res["user"] = PatientSerializer(tuple(patient)[0]).data
        elif len(guardian) != 0:
            res["type"] = "guardian"
            res["user"] = GuardianSerializer(tuple(guardian)[0]).data
        else:
            res["type"] = "nothing"
            res["user"] = UserSerializer(user).data

        return Response(res, status=status.HTTP_200_OK)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


class PatientSettingViewSet(viewsets.ModelViewSet):
    queryset = PatientSetting.objects.all()
    serializer_class = PatientSettingSerializer
    # permission_classes = [IsAuthenticated]


class GuardianViewSet(viewsets.ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        # raise Exception(request.user, type(request.user))
        user: User = request.user
        return resp


class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    # permission_classes = [IsAuthenticated]


class TokensViewSet(viewsets.ModelViewSet):
    queryset = Tokens.objects.all()
    serializer_class = TokensSerializer


class TranzactionViewSet(viewsets.ModelViewSet):
    queryset = Tranzaction.objects.all()
    serializer_class = TranzactionSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Doctor.objects.filter(patient__user=self.request.user.id)

    def create(self, request, *args, **kwargs):
        doc = create_doctor(list(request.data.values()) + [request.user.patient.id])
        return Response({'id': doc.id})

    def update(self, request, *args, **kwargs):
        doc_pk = self.kwargs['pk']
        update_doctor(request.user.patient.id, doc_pk, **request.data)
        return Response('OK')

    def destroy(self, request, *args, **kwargs):
        doc_pk = self.kwargs['pk']
        delete_doctor(request.user.patient.id, doc_pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        doc_pk = self.kwargs['pk']
        doctor = get_doctor(request.user.patient.id, doc_pk)
        serializer = self.get_serializer(doctor)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        doctors = list_doctors(request.user.patient.id)
        serializer = self.get_serializer(doctors, many=True)
        return Response(serializer.data)


class DoctorVisitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DoctorVisit.objects.filter(patient__user=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadOnlyDoctorVisitSerializer
        else:
            return DoctorVisitSerializer
