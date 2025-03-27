from django.contrib import admin
from api.models import  Patient, Doctor, PatientDoctorMapping

# Register your models here.
admin.site.register (Patient)
admin.site.register(Doctor)
admin.site.register(PatientDoctorMapping)
