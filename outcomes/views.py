from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Outcome_details
from .serializers import OutcomeSerializer

class OutcomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Outcome cases with:
    - Dynamic filtering
    - Stats endpoint for charts
    """
    queryset = Outcome_details.objects.all()
    serializer_class = OutcomeSerializer

    def get_queryset(self):
        queryset = Outcome_details.objects.all()
        outcome_param = self.request.query_params.get('outcome')
        if outcome_param:
            queryset = queryset.filter(outcome__iexact=outcome_param)
        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Outcome cases"""
        data = {}

        # Count occurrences per outcome
        data['outcome'] = {
            item['outcome']: item['count']
            for item in Outcome_details.objects.values('outcome')
                .annotate(count=Count('id'))
                .order_by('-count')
        }

        return Response(data)
