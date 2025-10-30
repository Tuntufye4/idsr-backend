from rest_framework import viewsets
from .models import Facility
from .serializers import FacilitySerializer
from rest_framework.decorators import action  

class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer                                    