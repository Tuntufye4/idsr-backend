from rest_framework import viewsets
from .models import Facility
from .serializers import FacilitySerializer
from rest_framework.decorators import action  
from django.db.models import Count
from rest_framework.response import Response

class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer                                    

    def get_queryset(self):
        queryset = Facility.objects.all()
        case_source  = self.request.query_params.get('case_source')
        reporting_method = self.request.query_params.get('reporting_method')   
        health_facility_code = self.request.query_params.get('health_facility_code')    
        designation = self.request.query_params.get('designation') 

        if case_source:
            queryset = queryset.filter(case_source__iexact=case_source)

        if reporting_method:
            queryset = queryset.filter(reporting_method__icontains=reporting_method)

        if health_facility_code:
            queryset = queryset.filter(health_facility_code__icontains=health_facility_code)

        if designation:
            queryset = queryset.filter(designation__icontains=designation)


        return queryset     
   
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Facility"""
        data = {}   

        # Facility counts
        data['casesource'] = (
            Facility.objects.values('case_source')
            .annotate(count=Count('id'))
            .order_by('-count')
        )


        # You can easily add more analytics:
        data['reportingmethod'] = (
            Facility.objects.values('reporting_method')
            .annotate(count=Count('id'))
            .order_by('-count')
        )


        return Response(data)
   
   
                                              