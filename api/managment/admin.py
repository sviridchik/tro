from django.contrib import admin
from .models import Patient,PatientSetting,Report,ReportDot
# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass

@admin.register(PatientSetting)
class PatientSettingAdmin(admin.ModelAdmin):
    pass

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass

@admin.register(ReportDot)
class ReportDotAdmin(admin.ModelAdmin):
    pass
