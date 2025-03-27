from django.urls import path
from .views import (
    register,login,
    patient_list_create, patient_retrieve_update_destroy, 
    doctor_list_create, doctor_retrieve_update_destroy, 
    patient_doctor_mapping_list_create, patient_doctor_mapping_retrieve_destroy
)

urlpatterns = [
    # Authentication Endpoints
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    
    # Patient Endpoints
    path('patients/', patient_list_create, name='patient-list-create'), 
    path('patients/<int:pk>/', patient_retrieve_update_destroy, name='patient-detail'),  # Retrieve, Update, Delete

    # Doctor Endpoints
    path('doctors/', doctor_list_create, name='doctor-list-create'),  # List and Create
    path('doctors/<int:pk>/', doctor_retrieve_update_destroy, name='doctor-detail'),  # Retrieve, Update, Delete

    # Patient-Doctor Mapping Endpoints
    path('mappings/', patient_doctor_mapping_list_create, name='mapping-list-create'),  # List and Create
    path('mappings/<int:pk>/', patient_doctor_mapping_retrieve_destroy, name='mapping-detail'),  # Retrieve and Delete
]
