# models.py (Django backend updated for full patient data model)
import uuid   
from django.db import models
from patients.models import PatientCase

class Lab(models.Model):
    patient_id = models.ForeignKey(    
        PatientCase,
        on_delete=models.SET_NULL,    
        null=True,            
        related_name='lab'  # <-- unique reverse name    
    )         
    specimen_collected = models.BooleanField(default=False)
    date_specimen_collected = models.DateField(blank=True, null=True)
    specimen_type = models.CharField(max_length=100, blank=True, null=True)
    lab_name = models.CharField(max_length=200, blank=True, null=True)
    specimen_sent_to_lab = models.BooleanField(default=False)              
    lab_result = models.CharField(max_length=200, blank=True, null=True)
    lab_tests_ordered = models.CharField(max_length=200, blank=True, null=True)  
   
    def __str__(self):      
        patient_name = self.patient_id.full_name if self.patient_id else "Unknown Patient"
        return f"{patient_name} ({self.id})"          
                                            