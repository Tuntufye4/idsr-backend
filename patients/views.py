from rest_framework import viewsets
from .models import PatientCase
from .serializers import PatientCaseSerializer

class PatientCaseViewSet(viewsets.ModelViewSet):
    queryset = PatientCase.objects.all()
    serializer_class = PatientCaseSerializer
   