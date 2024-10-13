from datetime import datetime
from pytz import timezone
import pprint
import json
from django.shortcuts import render, render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import (
    Specialization, 
    Appointment, 
    DoctorAvailability,
    Medication,
    Prescription,
)
from auth_app.models import CustomUser


class PatientHomeView(LoginRequiredMixin, View):
    template_name = 'patient/patient_home.html'

    def get(self, request, *args, **kwargs):
        profile = CustomUser.objects.get(id = request.user.id)
        context = {
            'patient': profile,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
        }
        return render(request,self.template_name, context)
    

class PatientProfileView(LoginRequiredMixin, View):
    template_name = 'patient/patient_profile.html'

    def get(self, request):
        profile = CustomUser.objects.get(id = request.user.id)
        context = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'phone_number': profile.phone_number,
        }
        return render(request, self.template_name, context)


class ViewResourcesView(LoginRequiredMixin, View):
    template_name = 'patient/patient_resources.html'

    def get(self, request):
        profile = CustomUser.objects.get(id = request.user.id)
        context = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
        }
        return render(request, self.template_name, context)


class PatientMedicalHistoryView(LoginRequiredMixin, View):
    template_name = 'patient/patient_medical_history.html'

    def get(self, request, *args, **kwargs):
        profile = CustomUser.objects.get(id = request.user.id)
        appointments = Appointment.objects.filter(patient=request.user).order_by('-id')
        medications = Medication.objects.filter(appointment__patient=request.user)
        prescriptions = Prescription.objects.filter(appointment__in=appointments)
        prescriptions_list = []
        for prescription in prescriptions:
            appointment = prescription.appointment
            patient = appointment.patient
            prescription_data = {
            'id': prescription.id,
            'diagnosis': prescription.diagnosis,
            'appointment_id': appointment.id,
            'appointment_date': appointment.appointment_date,
            'doctor_id': appointment.doctor.id,
            'doctor_name': f"Dr. {appointment.doctor.first_name} {appointment.doctor.last_name}",
            'patient_id': patient.id,
            'patient_name': f"{patient.first_name} {patient.last_name}",
            }
            prescriptions_list.append(prescription_data)
        
        print(f"Prescriptions: {prescriptions_list}")
        context = {
            'patient_id': request.user.id,
            'appointments': appointments,
            'medications': medications,
            'prescriptions': prescriptions_list,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
        }
        return render(request, self.template_name, context)
    

class PatientAppointmentHistoryView(LoginRequiredMixin, View):
    template_name = 'patient/patient_appointment_history.html'

    def get(self, request, *args, **kwargs):
        profile = CustomUser.objects.get(id = request.user.id)
        appointments = Appointment.objects.filter(patient=request.user).order_by('-id')
        context = {
            'patient_id': request.user.id,
            'appointments': appointments,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
        }
        return render(request, self.template_name, context)


class DoctorsListView(LoginRequiredMixin, View):
    template_name = 'doctors_list.html'
    
    def get(self, request):
        dept = request.GET.get('speciality', None)
        print(f"Department: {dept}")
        if dept:
            doctors = CustomUser.objects.filter(role='doctor', specialization__specialization=dept)
            india = timezone('Asia/Kolkata')
            today = datetime.now(india).strftime('%Y-%m-%d')
            doctors_with_slots = []
            for doctor in doctors:
                slots = DoctorAvailability.objects.filter(doctor=doctor, day=today).first()
                if slots:
                    doctors_with_slots.append({
                        'doctor': doctor,
                        'time_slots': slots.time_slots
                    })
            print(f"Doctors with slots: {doctors_with_slots}")

        else:
            doctors = CustomUser.objects.filter(role='doctor')

        context = {
            'doctors': doctors_with_slots,
        }
        # availability = doctors.first().doctoravailability_set.all()
        # print(f"availability: {availability}")
        return render(request, self.template_name, context)


class AppointmentTimeView(LoginRequiredMixin, View):
    template_name = 'appointment_time.html'
    
    def get(self, request):
        doctor_id = request.GET.get('doctor_id', None)
        if doctor_id:
            time_slots = ['9:00 AM - 9:30 AM', '10:00 AM - 10:30 AM', '11:00 AM - 11:30 AM', '2:00 PM - 2:30 PM']
        else:
            time_slots = ['9:00 AM - 9:30 AM', '10:00 AM - 10:30 AM', '11:00 AM - 11:30 AM', '2:00 PM - 2:30 PM']
        return render(request, self.template_name, {'time_slots': time_slots})
    

class DoctorHomeView(LoginRequiredMixin, View):
    template_name = 'doctor_dashboard.html'

    def get(self, request):
        india = timezone('Asia/Kolkata')
        today = datetime.now(india).strftime('%Y-%m-%d')
        doctor_id = request.user.id
        profile = CustomUser.objects.get(id=doctor_id)
        specialization = Specialization.objects.filter(user=doctor_id).first()
        appointments = None
        slots = DoctorAvailability.objects.filter(doctor=doctor_id, day=today).first()
        time_slots = slots.time_slots if slots else None
        context = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'appointments': appointments,
            'specialization': specialization.specialization,
            'slots': time_slots,
        }
        return render(request, self.template_name, context)
    

class DoctorProfileView(LoginRequiredMixin, View):
    template_name = 'doctor_profile.html'

    def get(self, request):
        doctor_id = request.user.id
        profile = CustomUser.objects.get(id = doctor_id)
        print(f"Profile: {profile}")
        specialization = Specialization.objects.filter(user = doctor_id).first()
        context = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'phone_number': profile.phone_number,
            'qualification': specialization.qualification if specialization else None,
            'specialization': specialization.specialization if specialization else None,
            'fee': specialization.fee if specialization else None,
        }
        return render(request, self.template_name, context)


class PatientManagementView(LoginRequiredMixin, View):
    template_name = 'patient_management.html'

    def get(self, request):
        appointments = Appointment.objects.filter(doctor=request.user).order_by('-id')
        profile = CustomUser.objects.get(id=request.user.id)

        context = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'appointments': appointments,
            'email': profile.email,
        }
        return render(request, self.template_name, context)


class DoctorAvailabilityView(LoginRequiredMixin, View):
    template_name = 'doctor_availability.html'

    def get(self, request):
        india = timezone('Asia/Kolkata')
        today = datetime.now(india).strftime('%Y-%m-%d')
        doctor_id = request.user.id
        slots = DoctorAvailability.objects.filter(doctor=doctor_id, day=today).first()
        profile = CustomUser.objects.get(id = doctor_id)
        print(f"Profile: {profile}")
        specialization = Specialization.objects.filter(user = doctor_id).first()
        context = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'phone_number': profile.phone_number,
            'qualification': specialization.qualification if specialization else None,
            'specialization': specialization.specialization if specialization else None,
            'fee': specialization.fee if specialization else None,
        }
        time_slots = slots.time_slots if slots else None
        if not slots:
            time_slots = [
                {"start_time": "9:00 AM", 
                "end_time": "12:00 PM", 
                "status": "Not Available"},
                {"start_time": "1:00 PM",
                "end_time": "4:00 PM",
                "status": "Not Available"},
                {"start_time": "5:00 PM",
                "end_time": "8:00 PM",
                "status": "Not Available"},
            ]

            DoctorAvailability.objects.create(doctor=request.user, day=today, time_slots=time_slots)
        context["slots"] = time_slots
        return render(request, self.template_name, context)


@require_POST
@login_required
def update_profile(request):
    profile = CustomUser.objects.get(id = request.user.id)
    profile.first_name = request.POST.get('first_name', profile.first_name)
    profile.last_name = request.POST.get('last_name', profile.last_name)
    profile.email = request.POST.get('email', profile.email)
    profile.phone_number = request.POST.get('phone_number', profile.phone_number)
    profile.save()

    specialization_text = request.POST.get('specialization', None)
    fee = request.POST.get('fee', None)
    qualification = request.POST.get('qualification', None)
    
    if specialization_text or fee:
        specialization_obj, created = Specialization.objects.get_or_create(user=profile)
        if specialization_text:
            specialization_obj.specialization = specialization_text
        if fee:
            specialization_obj.fee = fee
        if qualification:
            specialization_obj.qualification = qualification
        
        specialization_obj.save()
    
    
    response_data = {
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'email': profile.email,
        'phone_number': profile.phone_number,
        'qualification': specialization_obj.qualification or 'No Qualification added',
        'specialization': specialization_obj.specialization or 'No Specialization added',
        'fee': specialization_obj.fee or 'No Consultation fee added',
    }
    
    return JsonResponse(response_data)


@require_POST
@login_required
def update_doctor_availability(request):
    doctor_id = request.user.id
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    # Print request body
    print("Request Body:")
    pprint.pprint(data)
    response_data = []
    availability_list = data.get('availability', [])
    availability_list_for_db = []
    for availability_entry in availability_list:
        start_time_str = availability_entry.get('start_time', None)
        end_time_str = availability_entry.get('end_time', None)
        status = availability_entry.get('status', None)
        
        print(f"Processing availability for start_time: {start_time_str}, end_time: {end_time_str}")
        
        if status and start_time_str and end_time_str:
            availability_list_for_db.append({
                'start_time': start_time_str,
                'end_time': end_time_str,
                'status': status
            })
    india = timezone('Asia/Kolkata')
    today = datetime.now(india).strftime('%Y-%m-%d')
    availability = DoctorAvailability.objects.filter(doctor=doctor_id, day=today).first()
    availability.time_slots = availability_list_for_db
    availability.save()

    response_data = availability_list_for_db
    
    return JsonResponse({'status': 'success', 'availability': response_data})


class ConfirmAppointmentView(LoginRequiredMixin, View):
    template_name = 'appointment_confirmation.html'

    def get(self, request):
        appointment_time = request.GET.get('time')
        doctor_id = request.GET.get('doctor_id')
        
        if not appointment_time or not doctor_id:
            return JsonResponse({'error': 'Missing appointment time or doctor ID'}, status=400)
        
        india = timezone('Asia/Kolkata')
        today = datetime.now(india).strftime('%Y-%m-%d')
        doctor = get_object_or_404(CustomUser, id=doctor_id)
        slots = DoctorAvailability.objects.filter(doctor=doctor_id, day=today).first()
        specialization = Specialization.objects.filter(user=doctor_id).first()
        appointment = Appointment.objects.create(patient=request.user, doctor=doctor, department=specialization.specialization, appointment_date=today, appointment_time=appointment_time)
        context = {
            'appointment_id': appointment.id,
            'patient_name': request.user.first_name,
            'doctor_name': f"Dr. {doctor.first_name} {doctor.last_name}",
            'department': specialization.specialization if specialization else None,
            'fee': specialization.fee if specialization else None,
            'appointment_time': appointment_time,
        }

        return render(request, self.template_name, context)


@login_required
def cancel_appointment(request):
    appointment_id = request.GET.get('appointment_id')
    if not appointment_id:
        return JsonResponse({'error': 'Missing appointment ID'}, status=400)
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'cancelled'
    appointment.save()
    
    return JsonResponse({'status': 'success'})


class ViewAppointmentView(LoginRequiredMixin, View):
    template_name = 'patient_details.html'
    
    def get(self, request):
        appointment_id = request.GET.get('appointment_id')
        if not appointment_id:
            return JsonResponse({'error': 'Missing appointment ID'}, status=400)
        
        appointment = get_object_or_404(Appointment, id=appointment_id)
        context = {
            'appointment': appointment,
            'patient': appointment.patient,
            'doctor': appointment.doctor,
        }
        return render(request, self.template_name, context)
    

class PrescribeView(LoginRequiredMixin, View):
    template_name = 'prescribe.html'

    def get(self, request):
        appointment_id = request.GET.get('appointment_id')
        if not appointment_id:
            return JsonResponse({'error': 'Missing appointment ID'}, status=400)
        
        appointment = get_object_or_404(Appointment, id=appointment_id)
        medications = Medication.objects.filter(appointment=appointment)
        medications_list = list(medications.values())
        prescription = Prescription.objects.filter(appointment=appointment).first()

        context = {
            'appointment': appointment,
            'patient': appointment.patient,
            'doctor': appointment.doctor,
            'medications': medications_list,
            'diagnosis': prescription.diagnosis if prescription else None,
        }
        return render(request, self.template_name, context)
    

@login_required
def add_medication(request):
    print(f"reached add_medication")
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    appointment_id = data.get('appointment_id')
    medication = data.get('medication')
    dosage = data.get('dosage')
    frequency = data.get('frequency')
    duration = data.get('duration')
    if not appointment_id or not medication:
        return JsonResponse({'error': 'Missing appointment ID or medication'}, status=400)
    
    medication_entry = Medication.objects.create(
        appointment_id=appointment_id, 
        medication=medication, 
        dosage=dosage, 
        frequency=frequency, 
        duration=duration
    )
    
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.medication = medication_entry
    appointment.save()
    
    return JsonResponse({'status': 'success'})


@login_required
def remove_medication(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    medication_id = data.get('med_id')
    if not medication_id:
        return JsonResponse({'error': 'Missing medication ID'}, status=400)
    
    medication = get_object_or_404(Medication, id=medication_id)
    medication.delete()
    
    return JsonResponse({'status': 'success'})


@login_required
def save_prescription(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    appointment_id = data.get('appointment_id')
    diagnosis = data.get('diagnosis')
    if not appointment_id or not diagnosis:
        return JsonResponse({'error': 'Missing appointment ID or diagnosis'}, status=400)
    
    prescription, created = Prescription.objects.update_or_create(
        appointment_id=appointment_id,
        defaults={
            'diagnosis': diagnosis,    # Fields to update if the record exists
        }
    )    
    return JsonResponse({'status': 'success'})


class ViewPrescriptionView(LoginRequiredMixin, View):
    template_name = 'view_prescription.html'

    def get(self, request, id):
        appointment_id = id
        if not appointment_id:
            return JsonResponse({'error': 'Missing appointment ID'}, status=400)
        
        appointment = get_object_or_404(Appointment, id=appointment_id)
        medications = Medication.objects.filter(appointment=appointment)
        medications_list = medications.values()
        prescription = Prescription.objects.filter(appointment=appointment).first()

        context = {
            'appointment': appointment,
            'patient': appointment.patient,
            'doctor': appointment.doctor,
            'medications': medications_list,
            'diagnosis': prescription.diagnosis if prescription else None,
        }
        return render(request, self.template_name, context)
    

#Admin views

class AdminHomeView(LoginRequiredMixin, View):
    template_name = 'admin/admin_dashboard.html'

    def get(self, request):
        user_id = request.user.id
        profile = CustomUser.objects.get(id = user_id)
        context = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'phone_number': profile.phone_number,
        }
        return render(request, self.template_name, context)
    

class AdminProfileView(LoginRequiredMixin, View):
    template_name = 'admin/admin_profile.html'

    def get(self, request):
        admin_id = request.user.id
        profile = CustomUser.objects.get(id = admin_id)
        context = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'phone_number': profile.phone_number,
        }
        return render(request, self.template_name, context)
    

class AdminDoctorsListView(LoginRequiredMixin, View):
    template_name = 'admin/admin_doctors_list.html'

    def get(self, request):
        doctors = CustomUser.objects.filter(role='doctor')
        doctors_with_specializations = []

        for doctor in doctors:
            specialization = Specialization.objects.filter(user=doctor).first()
            doctor_info = {
                'id': doctor.id,
                'first_name': doctor.first_name,
                'last_name': doctor.last_name,
                'email': doctor.email,
                'phone_number': doctor.phone_number,
                'specialization': specialization if specialization else None
            }
            doctors_with_specializations.append(doctor_info)

        context = {
            'doctors': doctors_with_specializations,
        }
        print(f"Context: {context}")
        return render(request, self.template_name, context)
    

class AdminPatientsListView(LoginRequiredMixin, View):
    template_name = 'admin/admin_patients_list.html'

    def get(self, request):
        patients = CustomUser.objects.filter(role='patient')
        context = {
            'patients': patients,
        }
        return render(request, self.template_name, context)
    

class AdminAppointmentsListView(LoginRequiredMixin, View):
    template_name = 'admin/admin_appointments_list.html'

    def get(self, request):
        appointments = Appointment.objects.all()
        context = {
            'appointments': appointments,
        }
        return render(request, self.template_name, context)
    

@require_POST
@login_required
def admin_update_profile(request):
    profile = CustomUser.objects.get(id = request.user.id)
    profile.first_name = request.POST.get('first_name', profile.first_name)
    profile.last_name = request.POST.get('last_name', profile.last_name)
    profile.phone_number = request.POST.get('phone_number', profile.phone_number)
    profile.save()

    response_data = {
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'phone_number': profile.phone_number
    }
    
    return JsonResponse(response_data)