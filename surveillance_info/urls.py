from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SurveillanceViewSet

router = DefaultRouter()
router.register(r'', SurveillanceViewSet, basename='surveillancecase')

urlpatterns = router.urls    
           