from rest_framework import routers

from .views import DeviseViewSet,LogsViewSet,MissedMedViewSet,TakenMedViewSet
router = routers.DefaultRouter()
router.register('devise', DeviseViewSet, basename='devise')
router.register('logs', LogsViewSet, basename='logs')
router.register('missed_med', MissedMedViewSet, basename='missed_med')
router.register('taken_med', TakenMedViewSet, basename='taken_med')

urlpatterns = []
urlpatterns += router.urls
