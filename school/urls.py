from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register('subjects', SubjectViewSet)
router.register('classes', ClassViewSet)
router.register('students', StudentViewSet)
router.register('teachers', TeacherViewSet)
router.register('marks', MarkViewSet)

urlpatterns = [
        path('api', include(router.urls)),

        path('dashboard/', DashboardNoSqlView.as_view(), name='dashboard_url'),
        path('dashboard-sql/', DashboardSqlView.as_view(), name='dashboard_sql_url'),

]