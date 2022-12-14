from rest_framework import serializers

from .models import Schedule, Cure, TimeTable


# from api.managment.serializers import PatientSerializer

class ScheduleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Schedule
        fields = ('id','cycle_start','cycle_end','frequency')


class MainTimeTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeTable
        fields = ("time",)


class TimeTableSerializer(serializers.ModelSerializer):

    def to_representation(self, model):
        return {
            'Schedule': ScheduleSerializer(model).data,
            'Time': MainTimeTableSerializer(model).data,
        }

    class Meta:
        model = TimeTable
        fields = "__all__"


class MainCureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        print('HEREEEE')
        print(self.context['request'].user)
        validated_data['patient'] = self.context['request'].user.patient
        print(validated_data)
        cure = super().create(validated_data)
        return cure

    class Meta:
        model = Cure
        fields = ('id', 'title', 'dose', 'dose_type', 'type', "schedule","food","strict_status")


class CureSerializer(serializers.ModelSerializer):

    def to_representation(self, model):
        return {
            'cure': MainCureSerializer(model).data,
            'timetable': TimeTableSerializer(model).data
        }

    class Meta:
        model = Cure
        fields = "__all__"


