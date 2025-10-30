from rest_framework import viewsets
from .models import SurveillanceInfo
from .serializers import SurveillanceSerializer
from rest_framework.decorators import action  

class SurveillanceViewSet(viewsets.ModelViewSet):
    queryset = SurveillanceInfo.objects.all()
    serializer_class = SurveillanceSerializer                               