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
)
from auth_app.models import CustomUser


class PatientHomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'patient_id': request.user.id
        }
        return render(request, 'patient_home.html', context)


class PatientMedicalHistoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        appointments = Appointment.objects.filter(patient=request.user).order_by('-id')
        context = {
            'patient_id': request.user.id,
            'appointments': appointments,
        }
        return render(request, 'patient_medical_history.html', context)


class DoctorsListView(LoginRequiredMixin, View):
    template_name = 'doctors_list.html'
    
    def get(self, request):
        dept = request.GET.get('speciality', None)
        print(f"Department: {dept}")
        if dept:
            doctors = CustomUser.objects.filter(role='doctor', specialization__specialization=dept)
            print(f"Doctor: {doctors}")
        else:
            doctors = CustomUser.objects.filter(role='doctor')

        context = {
            'doctors': doctors
        }
        print(f"availability: {doctors.first().doctoravailability_set.all()}")
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
            'appointments': appointments
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
    
