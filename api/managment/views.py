from rest_framework import viewsets

from .models import Patient,PatientSetting,Guardian,Tariff,Tokens,Tranzaction,Doctor,DoctorVisit
from .serializers import PatientSerializer, PatientSettingSerializer, GuardianSerializer, TariffSerializer, \
    TokensSerializer,TranzactionSerializer, DoctorVisitSerializer,DoctorSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientSettingViewSet(viewsets.ModelViewSet):
    queryset = PatientSetting.objects.all()
    serializer_class = PatientSettingSerializer


class GuardianViewSet(viewsets.ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer


class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer



class TokensViewSet(viewsets.ModelViewSet):
    queryset = Tokens.objects.all()
    serializer_class = TokensSerializer


class TranzactionViewSet(viewsets.ModelViewSet):
    queryset = Tranzaction.objects.all()
    serializer_class = TranzactionSerializer



class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorVisitViewSet(viewsets.ModelViewSet):
    queryset = DoctorVisit.objects.all()
    serializer_class = DoctorVisitSerializer
