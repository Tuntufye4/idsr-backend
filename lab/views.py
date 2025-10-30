from rest_framework import viewsets
from .models import Lab
from .serializers import LabSerializer
from rest_framework.decorators import action  

class LabViewSet(viewsets.ModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer     