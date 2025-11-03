from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Avg, Min, Max
from .models import ClinicalCase
from .serializers import ClinicalCaseSerializer   

class ClinicalCaseViewSet(viewsets.ModelViewSet): 
    queryset = ClinicalCase.objects.all()   
    serializer_class = ClinicalCaseSerializer   

    def get_queryset(self):
        queryset = ClinicalCase.objects.all()   
        outcome = self.request.query_params.get('outcome')
        symptoms = self.request.query_params.get('symptoms')
        triage_level = self.request.query_params.get('triage_level')
        diagnosis_type = self.request.query_params.get('diagnosis_type')
        admission_status = self.request.query_params.get('admission_status')
        final_case_classification = self.request.query_params.get('final_case_classification')
        contact_with_confirmed_case = self.request.query_params.get('contact_with_confirmed_case')
        case_classification = self.request.query_params.get('case_classification')

        if outcome:
            queryset = queryset.filter(outcome__iexact=outcome)

        if symptoms:
            queryset = queryset.filter(symptoms__icontains=symptoms)

        if triage_level:
            queryset = queryset.filter(triage_level__icontains=triage_level)

        if diagnosis_type:
            queryset = queryset.filter(diagnosis_type__icontains=diagnosis_type)

        if admission_status:
            queryset = queryset.filter(admission_status__icontains=admission_status)

        if final_case_classification:
            queryset = queryset.filter(final_case_classification__icontains=final_case_classification)

        if contact_with_confirmed_case:
            queryset = queryset.filter(contact_with_confirmed_case__icontains=contact_with_confirmed_case)

        if case_classification:
            queryset = queryset.filter(case_classification__icontains=case_classification)

        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Clinical case"""
        data = {}

        # Outcome counts
        data['outcome'] = (
            ClinicalCase.objects.values('outcome')
            .annotate(count=Count('id'))
            .order_by('-count')
        )


        # You can easily add more analytics:
        data['symptoms'] = (
            ClinicalCase.objects.values('symptoms')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        data['triagelevel'] = (
            ClinicalCase.objects.values('triage_level')
            .annotate(count=Count('id'))
            .order_by('-count')
        )


        data['diagnosistype'] = (
            ClinicalCase.objects.values('diagnosis_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        
        data['caseclassification'] = (
            ClinicalCase.objects.values('case_classification')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        data['final_caseclassification'] = (
            ClinicalCase.objects.values('final_case_classification')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return Response(data)
   
    