from rest_framework import serializers

from .models import Devise, Logs, MissedMed, TakenMed


class DeviseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devise
        fields = "__all__"


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = "__all__"


class MissedMedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissedMed
        fields = "__all__"


class TakenMedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakenMed
        fields = "__all__"
