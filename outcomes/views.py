from rest_framework import viewsets
from .models import Outcome_details
from .serializers import OutcomeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response  
from django.db.models import Count
   
class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome_details.objects.all()   
    serializer_class = OutcomeSerializer                                                

    def get_queryset(self):
        queryset = Outcome_details.objects.all()
        outcome  = self.request.query_params.get('outcome')
       
        if outcome:
            queryset = queryset.filter(outcome__iexact=outcome)
   

        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Outcome"""
        data = {}

        # Outcome counts
        data['outcome'] = (
            Outcome_details.objects.values('outcome')
            .annotate(count=Count('id'))
            .order_by('-count')
        )


        return Response(data)
                                              