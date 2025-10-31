from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OutcomeViewSet

router = DefaultRouter()
router.register(r'outcomes', OutcomeViewSet, basename='outcomes')

urlpatterns = router.urls       
           