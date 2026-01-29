from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from .models import ClinicalCase
from .serializers import ClinicalCaseSerializer

class ClinicalCaseViewSet(viewsets.ModelViewSet):   
    """
    API endpoint for Clinical Cases with:
    - Dynamic filtering via query params
    - Stats endpoint for charts
    """
    queryset = ClinicalCase.objects.all()
    serializer_class = ClinicalCaseSerializer

    def get_queryset(self):
        queryset = ClinicalCase.objects.all()
        params = self.request.query_params

        # String filters
        string_fields = [
            'symptoms', 'triage_level', 'diagnosis_type', 'admission_status',
            'final_case_classification', 'case_classification', 'disease',
            'travel_destination'
        ]
        for field in string_fields:
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}__icontains": value})

        # Boolean filters
        bool_fields = ['contact_with_confirmed_case', 'recent_travel_history']
        for field in bool_fields:
            val = params.get(field)
            if val is not None:
                val_bool = val.lower() in ['true', '1', 'yes']
                queryset = queryset.filter(**{field: val_bool})

        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for charts"""
        data = {}

        # Helper function for generating counts dict
        def count_dict(field):
            return {item[field]: item['count'] for item in
                    ClinicalCase.objects.values(field).annotate(count=Count('id')).order_by('-count')}

        # String fields
        for field in ['symptoms', 'triage_level', 'diagnosis_type',
                      'case_classification', 'final_case_classification',
                      'admission_status', 'disease', 'travel_destination']:
            data[field] = count_dict(field)

        # Boolean fields
        for field in ['contact_with_confirmed_case', 'recent_travel_history']:
            counts = ClinicalCase.objects.values(field).annotate(count=Count('id'))
            # Convert True/False to Yes/No for frontend readability
            data[field] = {str(item[field]): item['count'] for item in counts}

        return Response(data)
