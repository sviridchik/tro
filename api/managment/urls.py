from rest_framework import routers

from .views import PatientViewSet, PatientSettingViewSet, GuardianViewSet, \
    TokensViewSet, TariffViewSet, TranzactionViewSet, LabelViewSet, AchievementViewSet

router = routers.DefaultRouter()
router.register('patients', PatientViewSet, basename='patients')
router.register('settings', PatientSettingViewSet, basename='settings')
router.register('guardians', GuardianViewSet, basename='guardians')
router.register('tokens', TokensViewSet, basename='tokens')
router.register('tariff', TariffViewSet, basename='settings')
router.register('tranzaction', TranzactionViewSet, basename='guardians')
router.register('label', LabelViewSet, basename='settings')
router.register('achievement', AchievementViewSet, basename='guardians')

urlpatterns = []
urlpatterns += router.urls
