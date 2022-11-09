from rest_framework import routers

from .views import CureViewSet, ScheduleViewSet, TimeTableViewSet

router = routers.DefaultRouter()
router.register('cure', CureViewSet, basename='cure')
router.register('schedule', ScheduleViewSet, basename='schedule')
router.register('time', TimeTableViewSet, basename='time')

urlpatterns = [
]
urlpatterns += router.urls
