# models.py (Django backend updated for full patient data model)
import uuid   
from django.db import models
from patients.models import PatientCase

class Facility(models.Model):
    patient_id =  models.ForeignKey(    
        PatientCase,
        on_delete=models.SET_NULL,    
        null=True,            
        related_name='facility'  # <-- unique reverse name    
    )  
    designation = models.CharField(max_length=100)
    date_reported = models.DateField(blank=True, null=True)
    form_completed_by = models.CharField(max_length=200)      
    health_facility_code = models.CharField(max_length=50)  
    case_source = models.CharField(max_length=70)     
    reporting_method = models.CharField(max_length=70)    
  
    def __str__(self):    
        patient_name = self.patient_id.full_name if self.patient_id else "Unknown Patient"
        return f"{patient_name} ({self.id})"            
                                                                            
                                               