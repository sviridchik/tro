from rest_framework import routers

from .views import PatientViewSet, PatientSettingViewSet

router = routers.DefaultRouter()
router.register('patients', PatientViewSet, basename='patients')
router.register('settings', PatientSettingViewSet, basename='settings')

urlpatterns = []
urlpatterns += router.urls
