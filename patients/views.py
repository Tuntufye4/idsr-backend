from rest_framework import viewsets
from .models import PatientCase
from .serializers import PatientCaseSerializer
from rest_framework.decorators import action  
from django.db.models import Count
from rest_framework.response import Response

class PatientCaseViewSet(viewsets.ModelViewSet):
    queryset = PatientCase.objects.all()
    serializer_class = PatientCaseSerializer   
       
    def get_queryset(self):
        queryset = PatientCase.objects.all()
        sex = self.request.query_params.get('sex')
        region = self.request.query_params.get('region')   
        district = self.request.query_params.get('district')  
        village = self.request.query_params.get('village') 
        vaccination_status = self.request.query_params.get('vaccination_status')

        if sex:
            queryset = queryset.filter(sex__iexact=sex)

        if region:
            queryset = queryset.filter(region__icontains=region)

        if district:
            queryset = queryset.filter(district__icontains=district)

        if village:
            queryset = queryset.filter(village__icontains=village)

        if vaccination_status:
            queryset = queryset.filter(vaccination_status__icontains=vaccination_status)


        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Patient Case"""
        data = {}

        # Outcome counts
        data['sex'] = (
            PatientCase.objects.values('sex')
            .annotate(count=Count('id'))
            .order_by('-count')
        )


        # You can easily add more analytics:
        data['vaccinationstatus'] = (
            PatientCase.objects.values('vaccination_status')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return Response(data)