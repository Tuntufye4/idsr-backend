from rest_framework import viewsets
from .models import Epidemiological_details
from .serializers import EpidemiologicalSerializer
from rest_framework.decorators import action  
  
class EpidemiologicalViewSet(viewsets.ModelViewSet):
    queryset = Epidemiological_details.objects.all()
    serializer_class = EpidemiologicalSerializer  

    def get_queryset(self):
        queryset = Epidemiological_details.objects.all()
        environmental_risk_factors  = self.request.query_params.get('environmental_risk_factors')
        exposure_source = self.request.query_params.get('exposure_source')
        cluster_related = self.request.query_params.get('cluster_related')
      

        if environmental_risk_factors:
            queryset = queryset.filter(environmental_risk_factors__iexact=environmental_risk_factors)

        if exposure_source:
            queryset = queryset.filter(exposure_source__icontains=exposure_source)

        if cluster_related:
            queryset = queryset.filter(cluster_related__icontains=cluster_related)

        return queryset
   
                                              