from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TreatmentViewSet  

router = DefaultRouter()
router.register(r'treatment', TreatmentViewSet, basename='treatmentcase')

urlpatterns = router.urls    
          

          