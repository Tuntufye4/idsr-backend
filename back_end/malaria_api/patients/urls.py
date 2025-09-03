from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientCaseViewSet

router = DefaultRouter()
router.register(r'cases', PatientCaseViewSet, basename='patientcase')

urlpatterns = router.urls  
