from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
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

        if outcome:
            queryset = queryset.filter(outcome__iexact=outcome)

        if symptoms:
            queryset = queryset.filter(symptoms__icontains=symptoms)

        if triage_level:
            queryset = queryset.filter(triage_level__icontains=triage_level)

        if diagnosis_type:
            queryset = queryset.filter(diagnosis_type__icontains=diagnosis_type)

        return queryset
   
    