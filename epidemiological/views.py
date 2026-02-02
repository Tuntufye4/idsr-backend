from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from .models import Epidemiological_details
from .serializers import EpidemiologicalSerializer
from patients.models import PatientCase    

class EpidemiologicalViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Epidemiological details:
    - Dynamic filtering
    - PATCH by patient_id (creates if missing)
    - Stats endpoint for charts
    """
    queryset = Epidemiological_details.objects.all()
    serializer_class = EpidemiologicalSerializer

    def get_queryset(self):
        queryset = Epidemiological_details.objects.all()
        params = self.request.query_params

        # String filters
        string_fields = ['environmental_risk_factors', 'exposure_source', 'cluster_related']
        for field in string_fields:
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}__icontains": value})

        return queryset

    @action(
        detail=False,
        methods=['patch'],
        url_path=r'by-patient/(?P<patient_id>\d+)'
    )
    def patch_by_patient(self, request, patient_id=None):
        """
        PATCH by patient_id: create record if missing, update fields.
        """
        try:   
            patient = PatientCase.objects.get(patient_id=patient_id)
        except PatientCase.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create the epidemiological record for this patient
        epi_record, _ = Epidemiological_details.objects.get_or_create(patient_id=patient)

        # Only update fields provided in the request
        data = {k: v for k, v in request.data.items() if v is not None}   
        serializer = EpidemiologicalSerializer(epi_record, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for charts"""
        data = {}

        def count_dict(field):
            return {
                item[field]: item['count']
                for item in Epidemiological_details.objects.values(field)
                        .annotate(count=Count('id'))
                        .order_by('-count')
            }

        for field in ['environmental_risk_factors', 'exposure_source', 'cluster_related']:
            data[field] = count_dict(field)

        return Response(data)
