from django.contrib import admin
from .models import Patient, PatientSetting, Guardian, Tariff, Tokens, Tranzaction
# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass

@admin.register(PatientSetting)
class PatientSettingAdmin(admin.ModelAdmin):
    pass

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    pass

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    pass

@admin.register(Tokens)
class TokensAdmin(admin.ModelAdmin):
    pass

@admin.register(Tranzaction)
class TranzactionAdmin(admin.ModelAdmin):
    pass
