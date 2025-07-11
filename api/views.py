# api/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Patient, Doctor, PatientDoctorMapping
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def home_redirect(request):
    return redirect('dashboard')

# Register View
# def register_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         User.objects.create_user(username=username, email=email, password=password)
#         return redirect('login')
#     return render(request, 'register.html')

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        return redirect('dashboard')

    return render(request, 'register.html')


from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username exists first
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'User does not exist.')
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect password.')
            return redirect('login')

    return render(request, 'login.html')




@login_required(login_url='/login/')
def dashboard_view(request):
    return render(request, 'dashboard.html')


# Patients
def patient_list(request):
    patients = Patient.objects.filter(user=request.user)
    return render(request, 'patients.html', {'patients': patients})

def add_patient(request):
    if request.method == 'POST':
        Patient.objects.create(
            user=request.user,
            name=request.POST['name'],
            age=request.POST['age'],
            condition=request.POST['condition']
        )
        return redirect('patient_list')
    return render(request, 'add_patient.html')

from django.shortcuts import get_object_or_404

def patient_detail(request, id):
    patient = get_object_or_404(Patient, id=id, user=request.user)
    return render(request, 'patient_detail.html', {'patient': patient})

def update_patient(request, id):
    patient = get_object_or_404(Patient, id=id, user=request.user)
    if request.method == 'POST':
        patient.name = request.POST['name']
        patient.age = request.POST['age']
        patient.condition = request.POST['condition']
        patient.save()
        return redirect('patient_list')
    return render(request, 'update_patient.html', {'patient': patient})

def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id, user=request.user)
    patient.delete()
    return redirect('patient_list')


# Doctors
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors.html', {'doctors': doctors})

def add_doctor(request):
    if request.method == 'POST':
        Doctor.objects.create(
            name=request.POST['name'],
            specialty=request.POST['specialty']
        )
        return redirect('doctor_list')
    return render(request, 'add_doctor.html')

def doctor_detail(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    return render(request, 'doctor_detail.html', {'doctor': doctor})

def update_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    if request.method == 'POST':
        doctor.name = request.POST['name']
        doctor.specialty = request.POST['specialty']
        doctor.save()
        return redirect('doctor_list')
    return render(request, 'update_doctor.html', {'doctor': doctor})

def delete_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor.delete()
    return redirect('doctor_list')


# Mappings
def manage_mappings(request):
    patients = Patient.objects.filter(user=request.user)
    doctors = Doctor.objects.all()
    mappings = PatientDoctorMapping.objects.filter(patient__user=request.user)

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        doctor_ids = request.POST.getlist('doctor_ids')

        if patient_id and doctor_ids:
            for doc_id in doctor_ids:
                PatientDoctorMapping.objects.get_or_create(
                    patient_id=patient_id,
                    doctor_id=doc_id
                )
            messages.success(request, "Doctors assigned successfully.")
            return redirect('manage_mappings')
        else:
            messages.error(request, "Please select a patient and at least one doctor.")

    return render(request, 'mappings.html', {
        'patients': patients,
        'doctors': doctors,
        'mappings': mappings
    })



def view_patient_doctors(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    mappings = PatientDoctorMapping.objects.filter(patient=patient)
    return render(request, 'patient_doctors.html', {
        'patient': patient,
        'mappings': mappings
    })

def remove_mapping(request, id):
    mapping = get_object_or_404(PatientDoctorMapping, id=id, patient__user=request.user)
    mapping.delete()
    return redirect('manage_mappings')
