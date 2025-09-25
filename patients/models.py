# models.py (Django backend updated for full patient data model)

from django.db import models

class PatientCase(models.Model):
    patient_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=200)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    national_id = models.CharField(max_length=100, blank=True, null=True)

    village = models.CharField(max_length=200)
    traditional_authority = models.CharField(max_length=200)
    health_facility = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    region = models.CharField(max_length=100)

    date_onset_symptoms = models.DateField()
    date_first_seen = models.DateField()
    disease = models.CharField(max_length=200)
    case_classification = models.CharField(max_length=100)
    outcome = models.CharField(max_length=100)
    date_of_death = models.DateField(blank=True, null=True)

    diagnosis_type = models.CharField(max_length=100)
    specimen_collected = models.BooleanField(default=False)
    date_specimen_collected = models.DateField(blank=True, null=True)
    specimen_type = models.CharField(max_length=100, blank=True, null=True)
    lab_name = models.CharField(max_length=200, blank=True, null=True)
    specimen_sent_to_lab = models.BooleanField(default=False)
    lab_result = models.CharField(max_length=200, blank=True, null=True)
    date_result_received = models.DateField(blank=True, null=True)
    final_case_classification = models.CharField(max_length=100)

    vaccination_status = models.CharField(max_length=100)
    date_last_vaccination = models.DateField(blank=True, null=True)
    contact_with_confirmed_case = models.BooleanField(default=False)
    recent_travel_history = models.BooleanField(default=False)
    travel_destination = models.CharField(max_length=200, blank=True, null=True)

    reporter_name = models.CharField(max_length=200)
    designation = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    date_reported = models.DateField()
    form_completed_by = models.CharField(max_length=200)
    date_form_completed = models.DateField()

    reporting_week_number = models.IntegerField()    
    year = models.IntegerField()
    health_facility_code = models.CharField(max_length=50)
    district_code = models.CharField(max_length=50)     
    form_version = models.CharField(max_length=50)     

    observations = models.TextField(blank=True, null=True)    

    def __str__(self):    
        return f"{self.full_name} ({self.patient_id})"        
                                          