from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Epidemiological_details
from .serializers import EpidemiologicalSerializer

class EpidemiologicalViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Epidemiological details with:
    - Dynamic filtering
    - Stats endpoint for analytics/charts
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

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for charts"""
        data = {}

        # Helper function to return {key: count}
        def count_dict(field):
            return {item[field]: item['count'] for item in
                    Epidemiological_details.objects.values(field)
                    .annotate(count=Count('id'))
                    .order_by('-count')}

        for field in ['environmental_risk_factors', 'exposure_source', 'cluster_related']:
            data[field] = count_dict(field)

        return Response(data)
