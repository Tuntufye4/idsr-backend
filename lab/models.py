# models.py (Django backend updated for full patient data model)
import uuid   
from django.db import models

class Lab(models.Model):
    patient_id = models.CharField(max_length=50, unique=True, editable=False, default=uuid.uuid4)
    full_name = models.CharField(max_length=200)        
    specimen_collected = models.BooleanField(default=False)
    date_specimen_collected = models.DateField(blank=True, null=True)
    specimen_type = models.CharField(max_length=100, blank=True, null=True)
    lab_name = models.CharField(max_length=200, blank=True, null=True)
    specimen_sent_to_lab = models.BooleanField(default=False)
    lab_result = models.CharField(max_length=200, blank=True, null=True)
    lab_tests_ordered = models.CharField(max_length=200, blank=True, null=True)  

    def __str__(self):      
        return f"{self.full_name} ({self.patient_id})"        
                                            