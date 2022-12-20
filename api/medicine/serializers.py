from rest_framework import serializers

from .models import Schedule, Cure, TimeTable


class MainTimeTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeTable
        fields = ('time', 'id')


class MainScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ('cycle_start', 'cycle_end', 'frequency', 'timesheet')


class ViewOnlyScheduleSerializer(serializers.ModelSerializer):
    timesheet = MainTimeTableSerializer(many=True)

    class Meta:
        model = Schedule
        fields = ('cycle_start', 'cycle_end', 'frequency', 'timesheet')


class MainCureSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['patient'] = self.context['request'].user.patient
        cure = super().create(validated_data)
        return cure

    class Meta:
        model = Cure
        fields = ('id', 'title', 'dose', 'dose_type', 'type', "schedule", "food", "strict_status")


class ViewOnlyCureSerializer(serializers.ModelSerializer):
    schedule = ViewOnlyScheduleSerializer()

    class Meta:
        model = Cure
        fields = ('id', 'title', 'dose', 'dose_type', 'type', "schedule", "food", "strict_status")


# ?? IDK for 10 days reports
class CureSerializer(serializers.ModelSerializer):

    def to_representation(self, model):
        return {
            'cure': MainCureSerializer(model).data,
            'timetable': MainTimeTableSerializer(model).data
        }

    class Meta:
        model = Cure
        fields = "__all__"
