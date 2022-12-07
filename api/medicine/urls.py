from rest_framework import routers
from django.urls import path, include, re_path
from .views import CureViewSet, ScheduleViewSet, TimeTableViewSet,MainView,TimeTableView

router = routers.DefaultRouter()
router.register('cure', CureViewSet, basename='cure')
router.register('schedule', ScheduleViewSet, basename='schedule')
router.register('time', TimeTableViewSet, basename='time')
data_pattern = "(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"

urlpatterns = [
    path('screen/', MainView.as_view()),
    # re_path(f'timetable/(?P<date_data>{data_pattern})/$', TimeTableView.as_view()),
    re_path(f'timetable/', TimeTableView.as_view()),

]
urlpatterns += router.urls
