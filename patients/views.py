from rest_framework import viewsets
from .models import PatientCase
from .serializers import PatientCaseSerializer
from rest_framework.decorators import action  

class PatientCaseViewSet(viewsets.ModelViewSet):
    queryset = PatientCase.objects.all()
    serializer_class = PatientCaseSerializer
   

    @action(detail=False, methods=['get'], url_path='lab-result')
    def lab_results(self, request):
        """
        Returns case counts by lab_result.
        """
        data = (
            self.get_queryset()
            .values('lab_result')
            .annotate(count=Count('id'))
            .order_by('lab_result')
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='vaccine-status')
    def vaccine_status(self, request):
        """
        Returns case counts by vaccine_status.
        """
        data = (
            self.get_queryset()
            .values('vaccination_status')
            .annotate(count=Count('id'))
            .order_by('vaccination_status')
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='specimen-type')
    def specimens(self, request):
        """
        Returns case counts by specimen_type.
        """
        data = (
            self.get_queryset()
            .values('specimen_type')
            .annotate(count=Count('id'))
            .order_by('specimen_type')
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='disease-distribution')
    def disease_distribution(self, request):
        """
        Returns case counts by disease.
        """
        data = (
            self.get_queryset()
            .values('disease')
            .annotate(count=Count('id'))
            .order_by('disease')
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='observation')
    def observation(self, request):
        """
        Returns case counts by observation.
        """
        data = (
            self.get_queryset()
            .values('observations')   
            .annotate(count=Count('id'))
            .order_by('observations')
        )
        return Response(list(data))
    
    @action(detail=False, methods=['get'], url_path='statistics')
    def statistics(self, request):
        """
        Returns general statistics.
        """
        total_cases = self.get_queryset().count()
        male_cases = self.get_queryset().filter(sex='Male').count()
        female_cases = self.get_queryset().filter(sex='Female').count()  
        classification_prob = self.get_queryset().filter(Classification='Probable').count()
        classification_conf = self.get_queryset().filter(Classification='Confirmed').count()

        return Response({
            "total_cases": total_cases,   
            "male_cases": male_cases,
            "female_cases": female_cases,  
            "classification_prob": classification_prob,  
            "classification_conf": classification_conf, 
        })