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
    - PATCH auto-creates section if it doesn't exist
    - Stats endpoint
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

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        PATCH endpoint: create Epidemiological_details if it doesn't exist for patient_id
        """
        patient_id = request.data.get("patient_id")
        if not patient_id:
            return Response({"error": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = PatientCase.objects.get(id=patient_id)
        except PatientCase.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create epidemiological record for this patient
        epi_record, created = Epidemiological_details.objects.get_or_create(patient_id=patient)

        serializer = EpidemiologicalSerializer(epi_record, data=request.data, partial=True)
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
