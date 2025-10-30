from rest_framework import viewsets
from .models import Treatment
from .serializers import TreatmentSerializer   
from rest_framework.decorators import action  

class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer                                      