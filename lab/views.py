from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from .models import Lab
from .serializers import LabSerializer
from patients.models import PatientCase

class LabViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Lab cases:
    - Dynamic filtering
    - PATCH auto-creates a record if missing
    - Stats endpoint
    """
    queryset = Lab.objects.all()
    serializer_class = LabSerializer

    def get_queryset(self):
        queryset = Lab.objects.all()
        params = self.request.query_params

        # Filterable fields
        string_fields = [
            'specimen_type', 'lab_result', 'lab_tests_ordered', 
            'lab_name', 'specimen_collected', 'specimen_sent_to_lab'
        ]
        for field in string_fields:
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}__icontains": value})

        return queryset

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        PATCH endpoint: create Lab record if it doesn't exist for patient_id
        """
        patient_id = request.data.get("patient_id")
        if not patient_id:
            return Response({"error": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = PatientCase.objects.get(id=patient_id)
        except PatientCase.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create lab record for this patient
        lab_record, created = Lab.objects.get_or_create(patient_id=patient)

        serializer = LabSerializer(lab_record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Lab cases"""
        data = {}

        def count_dict(field):
            return {item[field]: item['count'] for item in
                    Lab.objects.values(field)
                        .annotate(count=Count('id'))
                        .order_by('-count')}

        for field in ['specimen_type', 'lab_result', 'lab_tests_ordered',
                      'lab_name', 'specimen_collected', 'specimen_sent_to_lab']:
            data[field] = count_dict(field)

        return Response(data)
     