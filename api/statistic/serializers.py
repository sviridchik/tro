from rest_framework import serializers

from .models import Devise, Logs, MissedMed, TakenMed,Label,Achievement

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


class MissedMedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissedMed
        fields = "__all__"


class TakenMedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakenMed
        fields = "__all__"
