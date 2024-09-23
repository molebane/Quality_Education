# your_project/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from main.views import RegionViewSet, SchoolViewSet, StudentViewSet, TestScoreViewSet  # Import viewsets

# Create a router and register your viewsets
router = DefaultRouter()
router.register(r'regions', RegionViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'students', StudentViewSet)
router.register(r'testscores', TestScoreViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token obtain
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT token refresh
    path('api/', include(router.urls)),  # API routes for your viewsets
    path('', include('main.urls')),  # Include the main app's URLs
]
