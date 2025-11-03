from rest_framework import viewsets
from .models import Treatment  
from .serializers import TreatmentSerializer   
from rest_framework.decorators import action  
from django.db.models import Count   
from rest_framework.response import Response
   
class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer  

    def get_queryset(self):
        queryset = Treatment.objects.all()   
        procedures_done  = self.request.query_params.get('procedures_done')
        follow_up_plan = self.request.query_params.get('follow_up_plan')  
        treatment_given = self.request.query_params.get('treatment_given')   

        if procedures_done:
            queryset = queryset.filter(procedures_done__iexact=procedures_done)

        if follow_up_plan:
            queryset = queryset.filter(follow_up_plan__icontains=follow_up_plan)

        if treatment_given:
            queryset = queryset.filter(treatment_given__icontains=treatment_given)

        return queryset                               

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Treatment"""
        data = {}   

        # Treament counts
        data['procedures_done'] = (
            Treatment.objects.values('procedures_done')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # You can easily add more analytics:
        data['followupplan'] = (   
            Treatment.objects.values('follow_up_plan')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        data['treatmentgiven'] = (
            Treatment.objects.values('treatment_given')
            .annotate(count=Count('id'))
            .order_by('-count')
        )


        return Response(data)
   
   
                                                   