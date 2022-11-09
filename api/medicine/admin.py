from django.contrib import admin
from .models import Schedule,Cure,TimeTable
# Register your models here.
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass

@admin.register(Cure)
class CureAdmin(admin.ModelAdmin):
    pass

@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    pass

