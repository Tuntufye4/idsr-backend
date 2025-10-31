from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EpidemiologicalViewSet

router = DefaultRouter()
router.register(r'epidemiological', EpidemiologicalViewSet, basename='epidemiological')

urlpatterns = router.urls    
  