from django.urls import path
from . import views
from .views import TestScoreChartDataView
from .views import export_students_excel
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegionViewSet, SchoolViewSet, StudentViewSet, TestScoreViewSet  # Reference main.views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegionViewSet, SchoolViewSet, StudentViewSet, TestScoreViewSet


# Create a router and register your viewsets
router = DefaultRouter()
router.register(r'regions', RegionViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'students', StudentViewSet)
router.register(r'testscores', TestScoreViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.student_list, name='student_list'),
    path('api/chart-data/', TestScoreChartDataView.as_view({'get': 'list'}), name='chart-data'),
    path('export-students-excel/', export_students_excel, name='export_students_excel'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token obtain
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT token refresh
    path('api/', include(router.urls)),  # Include your API routes
    path('export-students/', export_students_excel, name='export_students'),
    path('dropout-chart/', views.dropout_chart, name='dropout_chart'),
    path('enrollment-comparison/', views.enrollment_comparison_chart, name='enrollment_comparison_chart'),
]
