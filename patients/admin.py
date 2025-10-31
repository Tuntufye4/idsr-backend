from django.contrib import admin
from .models import PatientCase

@admin.register(PatientCase)
class PatientCaseAdmin(admin.ModelAdmin):
    list_display = (
        "patient_id", "full_name", "health_facility", "district",
        "outcome"
    )   
    search_fields = ("full_name", "patient_id", "district", "national_id")
    list_filter = ("district", "outcome", "health_facility")
                            