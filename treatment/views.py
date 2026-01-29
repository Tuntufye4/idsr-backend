from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Treatment
from .serializers import TreatmentSerializer

class TreatmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Treatment cases with:   
    - Dynamic filtering
    - Stats endpoint for analytics/charts
    """
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

    def get_queryset(self):
        queryset = Treatment.objects.all()
        params = self.request.query_params

        # Filterable fields
        string_fields = [
            'procedures_done', 'follow_up_plan', 'treatment_given', 'referral_facility'
        ]
        for field in string_fields:
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}__icontains": value})

        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Treatment cases"""
        data = {}

        # Helper to return {key: count} dictionary
        def count_dict(field):
            return {item[field]: item['count'] for item in
                    Treatment.objects.values(field)
                    .annotate(count=Count('id'))
                    .order_by('-count')}

        for field in ['procedures_done', 'follow_up_plan', 'treatment_given', 'referral_facility']:
            data[field] = count_dict(field)

        return Response(data)
