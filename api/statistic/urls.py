from django.urls import path
from rest_framework import routers

from .views import DeviseViewSet,LogsViewSet,MissedMedViewSet,TakenMedViewSet,\
    LabelViewSet,AchievementViewSet,AnalyticTakenView,AnalyticTakenGuardianView, ReportTakenGuardianView

router = routers.DefaultRouter()
router.register('devise', DeviseViewSet, basename='devise')
router.register('logs', LogsViewSet, basename='logs')
router.register('missed_med', MissedMedViewSet, basename='missed_med')
router.register('taken_med', TakenMedViewSet, basename='taken_med')
router.register('label', LabelViewSet, basename='label')
router.register('achievement', AchievementViewSet, basename='achievement')
urlpatterns = [
    path('analytic/', AnalyticTakenView.as_view()),
    path('report/', ReportTakenGuardianView.as_view()),
    path('guardin/analytic/', AnalyticTakenGuardianView.as_view()),
]
urlpatterns += router.urls
