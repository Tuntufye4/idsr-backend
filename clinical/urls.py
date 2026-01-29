from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClinicalCaseViewSet

router = DefaultRouter()
router.register(r'clinical', ClinicalCaseViewSet, basename='clinicalcase')

urlpatterns = router.urls  
  

    