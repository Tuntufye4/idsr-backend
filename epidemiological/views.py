from rest_framework import viewsets
from .models import Epidemiological_details
from .serializers import EpidemiologicalSerializer   
from rest_framework.decorators import action  
from django.db.models import Count
from rest_framework.response import Response
  
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
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Epidemiological"""
        data = {}

        # Env_risk_factors counts
        data['environmental_risk_factors'] = (
            Epidemiological_details.objects.values('environmental_risk_factors')
            .annotate(count=Count('id'))
            .order_by('-count')
        )


        # You can easily add more analytics:
        data['exposure_source'] = (
            Epidemiological_details.objects.values('exposure_source')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        data['cluster_related'] = (
            Epidemiological_details.objects.values('cluster_related')
            .annotate(count=Count('id'))
            .order_by('-count')
        )


        return Response(data)
   
   
                                              