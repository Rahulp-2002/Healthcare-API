from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import PatientSerializer, DoctorSerializer, PatientDoctorMappingSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

      
@csrf_exempt  # Disable CSRF for this view
def register(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({"message": "User registered successfully"}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
        
@csrf_exempt  # Disable CSRF for this view
def login(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            # Find the user and check password
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)


# Patient Management Views (List and Create)
@api_view(['GET', 'POST'])
def patient_list_create(request):
    if request.method == 'GET':
        patients = Patient.objects.filter(user=request.user)  # Only show patient's own records
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new patient and associate it with the logged-in user
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Automatically associate the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Patient Detail Views (Retrieve, Update, Delete)
@api_view(['GET', 'PUT', 'DELETE'])
def patient_retrieve_update_destroy(request, pk):
    try:
        patient = Patient.objects.get(pk=pk, user=request.user)  # Ensure the patient belongs to the logged-in user
    except Patient.DoesNotExist:
        return Response({'message': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient.delete()
        return Response({'message': 'Patient deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Doctor Management Views
@api_view(['GET', 'POST'])
def doctor_list_create(request):
    if request.method == 'GET':
        doctors = Doctor.objects.all()  # Get all doctor
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Doctor Detail Views (Retrieve, Update, Delete)
@api_view(['GET', 'PUT', 'DELETE'])
def doctor_retrieve_update_destroy(request, pk):
    try:
        doctor = Doctor.objects.get(pk=pk)
    except Doctor.DoesNotExist:
        return Response({'message': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        doctor.delete()
        return Response({'message': 'Doctor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Patient-Doctor Mapping Views (List and Create)
@api_view(['GET', 'POST'])
def patient_doctor_mapping_list_create(request):
    if request.method == 'GET':
        mappings = PatientDoctorMapping.objects.all()  # Get all patient-doctor mappings
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatientDoctorMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Patient-Doctor Mapping Detail Views (Retrieve and Delete)
@api_view(['GET', 'DELETE'])
def patient_doctor_mapping_retrieve_destroy(request, pk):
    try:
        mapping = PatientDoctorMapping.objects.get(pk=pk)
    except PatientDoctorMapping.DoesNotExist:
        return Response({'message': 'Mapping not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientDoctorMappingSerializer(mapping)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        mapping.delete()
        return Response({'message': 'Mapping deleted successfully'}, status=status.HTTP_204_NO_CONTENT)