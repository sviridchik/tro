from rest_framework import serializers

from .models import Patient, PatientSetting, Guardian, Tariff, Tokens, Tranzaction,Doctor,DoctorVisit


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = "__all__"


class PatientSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSetting
        fields = "__all__"


class TokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tokens
        fields = "__all__"


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = "__all__"


class TranzactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tranzaction
        fields = "__all__"




class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"

class DoctorVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorVisit
        fields = "__all__"
