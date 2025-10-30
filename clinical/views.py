from rest_framework import viewsets
from .models import ClinicalCase
from .serializers import ClinicalCaseSerializer
from rest_framework.decorators import action  

class ClinicalCaseViewSet(viewsets.ModelViewSet):
    queryset = ClinicalCase.objects.all()   
    serializer_class = ClinicalCaseSerializer