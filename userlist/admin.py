from django.contrib import admin

# Register your models here.
from .models import Patient, Doctor, AmslerGrid, Hospital

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(AmslerGrid)
admin.site.register(Hospital)
