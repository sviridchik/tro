from django.contrib import admin
from .models import Devise, Logs, MissedMed, TakenMed,Report,ReportDot


@admin.register(Devise)
class DeviseAdmin(admin.ModelAdmin):
    pass

@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    pass

@admin.register(MissedMed)
class MissedMedAdmin(admin.ModelAdmin):
    pass

@admin.register(TakenMed)
class TakenMedAdmin(admin.ModelAdmin):
    pass

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass

@admin.register(ReportDot)
class ReportDotAdmin(admin.ModelAdmin):
    pass
