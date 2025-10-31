from rest_framework import viewsets
from .models import Outcome_details
from .serializers import OutcomeSerializer
from rest_framework.decorators import action  

class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome_details.objects.all()
    serializer_class = OutcomeSerializer                                                