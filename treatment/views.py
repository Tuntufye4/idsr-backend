from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from .models import Treatment
from .serializers import TreatmentSerializer
from patients.models import PatientCase

class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        PATCH endpoint: update treatment fields or create if missing
        """
        patient_id = request.data.get("patient_id")
        if not patient_id:
            return Response({"error": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = PatientCase.objects.get(id=patient_id)
        except PatientCase.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create treatment record for this patient
        treatment_record, created = Treatment.objects.get_or_create(patient_id=patient)

        serializer = TreatmentSerializer(treatment_record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Return summary counts for charts
        """
        data = {}
        for field in ['treatment_given', 'procedures_done', 'follow_up_plan', 'referral_facility']:
            counts = Treatment.objects.values(field).annotate(count=Count('id'))
            data[field] = {item[field]: item['count'] for item in counts}
        return Response(data)
