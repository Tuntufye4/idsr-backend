# models.py (Django backend updated for full patient data model)
import uuid   
from django.db import models

class Treatment(models.Model):
    patient_id = models.CharField(max_length=50, unique=True, editable=False, default=uuid.uuid4)
    full_name = models.CharField(max_length=200)
    treatment_given = models.CharField(max_length=100, blank=True, null=True)
    procedures_done = models.CharField(max_length=200, blank=True, null=True)
    follow_up_plan = models.CharField(max_length=200, blank=True, null=True)
    referral_facility = models.CharField(max_length=200, blank=True, null=True)   

    def __str__(self):    
        return f"{self.full_name} ({self.patient_id})"  
                                             


                                     