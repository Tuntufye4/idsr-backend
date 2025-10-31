# models.py (Django backend updated for full patient data model)
import uuid   
from django.db import models

class Epidemiological_details(models.Model):
    patient_id = models.CharField(max_length=50, unique=True, editable=False, default=uuid.uuid4)
    full_name = models.CharField(max_length=200)        
    environmental_risk_factors = models.CharField(max_length=100, blank=True, null=True)
    exposure_source = models.CharField(max_length=200, blank=True, null=True)
    cluster_related = models.CharField(max_length=200, blank=True, null=True)        

    def __str__(self):      
        return f"{self.full_name} ({self.patient_id})"  