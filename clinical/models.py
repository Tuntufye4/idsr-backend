# models.py (Django backend updated for full patient data model)
import uuid   
from django.db import models

class ClinicalCase(models.Model):      
    patient_id = models.CharField(max_length=50, unique=True, editable=False, default=uuid.uuid4)
    full_name = models.CharField(max_length=200)   
    disease = models.CharField(max_length=200)
    date_of_onset = models.DateField(blank=True, null=True)
    case_classification = models.CharField(max_length=100)
    symptoms = models.CharField(max_length=200)    
    triage_level = models.CharField(max_length=100)
    diagnosis_type = models.CharField(max_length=100)    
    final_case_classification = models.CharField(max_length=100)
    admission_status = models.CharField(max_length=100)
    contact_with_confirmed_case = models.BooleanField(default=False)
    recent_travel_history = models.BooleanField(default=False)
    travel_destination = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):    
        return f"{self.full_name} ({self.patient_id})"        
                                          