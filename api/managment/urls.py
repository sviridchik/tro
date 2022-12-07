from rest_framework import routers

from .views import PatientViewSet, PatientSettingViewSet, GuardianViewSet, \
    TokensViewSet, TariffViewSet, TranzactionViewSet,\
    DoctorViewSet,DoctorVisitViewSet

router = routers.DefaultRouter()
router.register('patients', PatientViewSet, basename='patients')
router.register('settings', PatientSettingViewSet, basename='settings')
router.register('guardians', GuardianViewSet, basename='guardians')
router.register('tokens', TokensViewSet, basename='tokens')
router.register('tariff', TariffViewSet, basename='tariff')
router.register('tranzaction', TranzactionViewSet, basename='tranzaction')
router.register('doctor', DoctorViewSet, basename='doctor')
router.register('doctorvisit', DoctorVisitViewSet, basename='doctorvisit')

urlpatterns = []
urlpatterns += router.urls
