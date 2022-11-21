from rest_framework import viewsets

from .models import Patient,PatientSetting,Guardian,Tariff,Tokens,Tranzaction,Label,Achievement
from .serializers import PatientSerializer, PatientSettingSerializer, GuardianSerializer, TariffSerializer, \
    TokensSerializer,TranzactionSerializer,LabelSerializer,AchievementSerializer


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


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
