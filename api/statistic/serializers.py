from rest_framework import serializers

from .models import Devise, Logs, MissedMed, TakenMed, Label, Achievement
from medicine.models import Cure


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = "__all__"


class DeviseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devise
        fields = "__all__"


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = "__all__"


class MedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cure
        fields = "__all__"


class MissedMedSerializer(serializers.ModelSerializer):
    med = MedSerializer()

    class Meta:
        model = MissedMed
        fields = "__all__"


class TakenMedSerializer(serializers.ModelSerializer):
    med = MedSerializer()

    class Meta:
        model = TakenMed
        fields = "__all__"
