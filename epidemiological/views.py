from rest_framework import viewsets
from .models import Epidemiological_details
from .serializers import EpidemiologicalSerializer
from rest_framework.decorators import action  

class EpidemiologicalViewSet(viewsets.ModelViewSet):
    queryset = Epidemiological_details.objects.all()
    serializer_class = EpidemiologicalSerializer                                            