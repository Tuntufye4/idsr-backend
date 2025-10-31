from rest_framework import viewsets
from .models import Facility
from .serializers import FacilitySerializer
from rest_framework.decorators import action  

class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer                                    

    def get_queryset(self):
        queryset = Facility.objects.all()
        case_source  = self.request.query_params.get('case_source')
        reporting_method = self.request.query_params.get('reporting_method')   
        health_facility_code = self.request.query_params.get('health_facility_code')    

        if case_source:
            queryset = queryset.filter(case_source__iexact=case_source)

        if reporting_method:
            queryset = queryset.filter(reporting_method__icontains=reporting_method)

        if health_facility_code:
            queryset = queryset.filter(health_facility_code__icontains=health_facility_code)


        return queryset
   
                                              