from rest_framework import viewsets
from .models import Lab
from .serializers import LabSerializer
from rest_framework.decorators import action  

class LabViewSet(viewsets.ModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer        

    def get_queryset(self):
        queryset = Lab.objects.all()
        specimen_type  = self.request.query_params.get('specimen_type')
        lab_result = self.request.query_params.get('lab_result')   
        lab_tests_ordered = self.request.query_params.get('lab_tests_ordered')    

        if specimen_type:
            queryset = queryset.filter(specimen_type__iexact=specimen_type)

        if lab_result:
            queryset = queryset.filter(lab_result__icontains=lab_result)

        if lab_tests_ordered:
            queryset = queryset.filter(lab_tests_ordered__icontains=lab_tests_ordered)


        return queryset