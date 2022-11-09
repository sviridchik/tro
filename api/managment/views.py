from rest_framework import viewsets
from .models import Patient, PatientSetting,ReportDot,Report
from .serializers import PatientSerializer,PatientSettingSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientSettingViewSet(viewsets.ModelViewSet):
    queryset = PatientSetting.objects.all()
    serializer_class = PatientSettingSerializer

