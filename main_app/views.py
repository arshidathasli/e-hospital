from datetime import datetime
from pytz import timezone
import pprint
import json
from django.shortcuts import render, render, redirect, get_object_or_404
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django import forms
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .forms import PatientUpdateForm, AppointmentForm
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
        context = {
            'patient_id': request.user.id
        }
        return render(request, 'patient_medical_history.html', context)


class DoctorsListView(LoginRequiredMixin, View):
    template_name = 'doctors_list.html'
    
    def get(self, request):
        specialization = request.GET.get('speciality', None)
        if specialization:
            doctors = CustomUser.objects.filter(role='doctor')
        else:
            doctors = CustomUser.objects.filter(role='doctor')
        
        return render(request, self.template_name, {'doctors': doctors})


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
        doctor_id = request.user.id
        profile = CustomUser.objects.get(id=doctor_id)
        specialization = Specialization.objects.filter(user=doctor_id).first()
        appointments = None
        availability = None
        context = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'appointments': appointments,
            'specialization': specialization.specialization,
            'availability': availability
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
        context = {}
        return render(request, self.template_name, context)


class DoctorAvailabilityView(LoginRequiredMixin, View):
    template_name = 'doctor_availability.html'

    def get(self, request):
        india = timezone('Asia/Kolkata')
        today = datetime.now(india).strftime('%Y-%m-%d')
        slots = DoctorAvailability.objects.filter(doctor=request.user.id, day=today).first()
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
        time_slots = slots.time_slots if slots else None
        if not slots:
            time_slots = [
                {"start_time": "9:00 AM", 
                "end_time": "1:00 PM", 
                "status": "Not Available"},
                {"start_time": "2:00 PM",
                "end_time": "6:00 PM",
                "status": "Not Available"},
                {"start_time": "2:00 PM",
                "end_time": "6:00 PM",
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



#Above Classes are edited 


class AvailabilityForm(forms.Form):
    availability = forms.CharField(max_length=255, required=True, label='Update Availability')    

    

class PatientDetailsView(View):
    def get(self, request, patient_id):
        # Fetch the specific patient by ID
        patient = get_object_or_404(CustomUser, id=patient_id)
        return render(request, 'patient_details.html', {'patient': patient})  


class PatientAppointmentCancelView(View):
    def post(self, request, appointment_id):
        # Fetch the specific appointment by ID
        appointment = get_object_or_404(Appointment, id=appointment_id)
        
        # Cancel the appointment (you may want to mark it as canceled instead of deleting)
        appointment.is_canceled = True  # Assuming you have an 'is_canceled' field
        appointment.save()

        messages.success(request, 'The appointment has been successfully canceled.')
        return redirect('patient_management')  # Redirect to the patient management page or wherever you want  


class CancelAppointmentConfirmationView(View):
    def get(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        return render(request, 'cancel_appointment.html', {'appointment': appointment})
    

class PatientDetailsUpdateView(View):
    def get(self, request, patient_id):
        # Fetch the patient object or return a 404 error if not found
        patient = get_object_or_404(CustomUser, id=patient_id)
        # Initialize the form with the patient instance
        form = PatientUpdateForm(instance=patient)
        return render(request, 'patient_details_update.html', {'form': form, 'patient': patient})

    def post(self, request, patient_id):
        # Fetch the patient object or return a 404 error if not found
        patient = get_object_or_404(CustomUser, id=patient_id)
        # Bind the form to the request data and the patient instance
        form = PatientUpdateForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()  # Save the updated details
            messages.success(request, 'Patient details have been successfully updated.')
            return redirect('patient_management')  # Redirect to a management page or desired URL
        return render(request, 'patient_details_update.html', {'form': form, 'patient': patient})  # Render the form again with errors
    

class EPrescribingView(View):
    def get(self, request):
        # Render the E-Prescribing form on GET request
        return render(request, 'e_prescribing.html')

    def post(self, request):
        # Handle prescription submission on POST request
        patient_name = request.POST.get('patient-name')
        medication = request.POST.get('medication')
        dosage = request.POST.get('dosage')
        frequency = request.POST.get('frequency')
        pharmacy = request.POST.get('pharmacy')

        # Here, you can add logic to save the prescription to the database

        messages.success(request, 'Prescription sent to pharmacy!')
        return redirect('E-prescribing')  # Redirect to the same page after submission
    

class AdminHomeView(TemplateView):
    template_name = 'admin_home.html'  # Specify the template name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context if necessary
        return context


class AdminAppointmentManagementView(TemplateView):
    template_name = 'admin_appointment_management.html'  


class AppointmentEditView(View):
    def get(self, request, *args, **kwargs):
        appointment_id = kwargs.get('pk')  # Get the appointment ID from the URL
        appointment = get_object_or_404(Appointment, id=appointment_id)
        form = AppointmentForm(instance=appointment)  # Pre-fill the form with the appointment data
        return render(request, 'appointment_edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        appointment_id = kwargs.get('pk')
        appointment = get_object_or_404(Appointment, id=appointment_id)
        form = AppointmentForm(request.POST, instance=appointment)  # Bind the form to the posted data
        if form.is_valid():
            form.save()  # Save the updated appointment
            return redirect('admin_appointment_management')  # Redirect to the appointment management page
        return render(request, 'appointment_edit.html', {'form': form})    
    
class AppointmentCancelView(View):
    def post(self, request, *args, **kwargs):
        # Get the appointment ID from the request (assuming it's passed in the form)
        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Update the status of the appointment to 'cancelled'
        appointment.status = 'cancelled'
        appointment.save()

        # Redirect to the appointment management page or any other page
        return redirect(reverse('admin_appointment_management')) 

class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_app/appointment_add.html'  # Your template for adding appointments
    success_url = reverse_lazy('appointment_list')  # Redirect to appointment list after saving

    def form_valid(self, form):
        return super().form_valid(form)  # You can add any extra logic here if needed 


class UserManagementView(ListView):
    template_name = 'appointment_app/user_management.html'
    context_object_name = 'users'  # You can customize this as needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = CustomUser.objects.all()  # Fetch all patients
        context['doctors'] = Doctor.objects.all()    # Fetch all doctors
        return context
    
class UserPatientEditView(UpdateView):
    model = CustomUser
    form_class = PatientUpdateForm
    template_name = 'appointment_app/patient_edit.html'
    context_object_name = 'patient'
    success_url = reverse_lazy('user_management')  # Redirect to user management page after saving

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit Patient'  # Add context for the template if needed
        return context

class PatientDeleteView(DeleteView):
    model = CustomUser
    template_name = 'appointment_app/patient_confirm_delete.html'  # Create this template
    success_url = reverse_lazy('user_management')  # Redirect after deletion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object  # Pass the patient object to the template
        return context
    

