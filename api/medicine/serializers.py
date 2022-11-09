from rest_framework import serializers

from .models import Schedule, Cure, TimeTable


# from api.managment.serializers import PatientSerializer

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class MainTimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = "time"


class TimeTableSerializer(serializers.ModelSerializer):
    def to_representation(self, model):
        return {
            'Schedule': Schedule(model).data,
            'Time': MainTimeTableSerializer(model).data,
        }

    class Meta:
        model = TimeTable
        fields = "__all__"


class MainCureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = ('patient', 'title', 'dose', 'dose_type', 'type')


class CureSerializer(serializers.ModelSerializer):
    def to_representation(self, model):
        return {
            'cure': MainCureSerializer(model).data,
            'timetable': TimeTableSerializer(model).data
        }

    class Meta:
        model = Cure
        fields = "__all__"
