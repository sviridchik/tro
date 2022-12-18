from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Patient, PatientSetting, Guardian, Tariff, Tokens, Tranzaction, Doctor, DoctorVisit


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        guard = super().create(validated_data)
        return guard

    class Meta:
        model = Patient
        fields = "__all__"


class GuardianSerializer(serializers.ModelSerializer):
    # care_about = PatientSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        guard = super().create(validated_data)
        return guard

    class Meta:
        model = Guardian
        # fields = "__all__"
        exclude = ['is_send', 'banned']


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

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user.patient
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['patient'] = instance.patient
        return super().update(instance, validated_data)

    class Meta:
        model = Doctor
        fields = "__all__"
        extra_kwargs = {
            'patient': {'default': None},
        }


class DoctorVisitSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user.patient
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['patient'] = instance.patient
        return super().update(instance, validated_data)

    class Meta:
        model = DoctorVisit
        fields = "__all__"
        extra_kwargs = {
            'patient': {'default': None},
        }


class ReadOnlyDoctorVisitSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = DoctorVisit
        fields = "__all__"
        extra_kwargs = {
            'patient': {'default': None},
        }
