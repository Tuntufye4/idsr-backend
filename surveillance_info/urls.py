from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SurveillanceViewSet

router = DefaultRouter()
router.register(r'surveillance', SurveillanceViewSet, basename='surveillancecase')

urlpatterns = router.urls    
        