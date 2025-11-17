from rest_framework import viewsets
from .models import Lab
from .serializers import LabSerializer
from rest_framework.decorators import action  
from django.db.models import Count
from rest_framework.response import Response

class LabViewSet(viewsets.ModelViewSet):
    queryset = Lab.objects.all()   
    serializer_class = LabSerializer        

    def get_queryset(self):   
        queryset = Lab.objects.all()
        specimen_type  = self.request.query_params.get('specimen_type')
        lab_result = self.request.query_params.get('lab_result')   
        lab_tests_ordered = self.request.query_params.get('lab_tests_ordered')   
        lab_name = self.request.query_params.get('lab_name')  
        specimen_collected = self.request.query_params.get('specimen_collected') 
        specimen_sent_to_lab = self.request.query_params.get('specimen_sent_to_lab')         

        if specimen_type:
            queryset = queryset.filter(specimen_type__iexact=specimen_type)

        if lab_result:
            queryset = queryset.filter(lab_result__icontains=lab_result)

        if lab_tests_ordered:
            queryset = queryset.filter(lab_tests_ordered__icontains=lab_tests_ordered)

        if lab_name:
            queryset = queryset.filter(lab_name__icontains=lab_name)

        if specimen_collected:
            queryset = queryset.filter(specimen_collected__icontains=specimen_collected)

        if specimen_sent_to_lab:
            queryset = queryset.filter(specimen_sent_to_lab__icontains=specimen_sent_to_lab)


        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Lab"""
        data = {}   

        # Case counts per specimen_type
           
        data['specimentype'] = (
            Lab.objects.values('specimen_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )


        # Case counts per lab result 

        data['labresult'] = (
            Lab.objects.values('lab_result')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # Case counts per lab tests ordered  
        
        data['labtestsordered'] = (
            Lab.objects.values('lab_tests_ordered')
            .annotate(count=Count('id'))
            .order_by('-count')
        )    

        # Case counts per lab name 
        
        data['labname'] = (
            Lab.objects.values('lab_name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )   

        data['specimencollected'] = (
            Lab.objects.values('specimen_collected')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        data['specimensenttotlab'] = (
            Lab.objects.values('specimen_sent_to_lab')
            .annotate(count=Count('id'))
            .order_by('-count')      
        )
        return Response(data)
   
   
                                              