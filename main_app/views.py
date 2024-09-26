from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Doctor  # Assuming you have a Doctor model
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django import forms
from .models import Patient  # Ensure this model exists and is imported
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from .models import PatientAppointment  # Import your PatientAppointment model
from .forms import PatientUpdateForm  # Import your Patient update form
from .models import Appointment  # Import your Appointment model
from .forms import AppointmentForm  # Import your Appoint
from .models import Facility
from .forms import FacilityForm  
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import CreateView
from .forms import PatientForm  # Ensure you have a form defined for Patient
from .forms import DoctorForm  # Import the form class for Doctor
















class PatientHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'patient_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any context you want to pass to the template, for example, patient's id
        context['patient_id'] = self.request.user.id  # Assuming the logged-in user is a patient
        return context

class DoctorsListView(ListView):
    model = Doctor
    template_name = 'doctors_list.html'
    context_object_name = 'doctors'

    # Optionally, you can override get_queryset to add filtering or ordering
    def get_queryset(self):
        return Doctor.objects.all()
    
class TakeAppointmentView(View):
    template_name = 'take_appointment.html'

    def get(self, request):
        # Available time slots (this can be fetched from the database)
        time_slots = ['9:00 AM - 9:30 AM', '10:00 AM - 10:30 AM', '11:00 AM - 11:30 AM', '2:00 PM - 2:30 PM']
        
        # Render the template with available time slots
        return render(request, self.template_name, {'time_slots': time_slots})

    def post(self, request):
        selected_time = request.POST.get('appointment_time')
        
        if selected_time:
            # Handle the logic of saving the appointment to the database here
            # For example:
            # Appointment.objects.create(user=request.user, time=selected_time)

            messages.success(request, f'Appointment booked for {selected_time}.')
            return redirect('proceed_payment')  # Redirect to a success page after booking
        else:
            messages.error(request, 'Please select a valid time slot.')
            return redirect('take_appointment')
        
class AvailabilityForm(forms.Form):
    availability = forms.CharField(max_length=255, required=True, label='Update Availability')        

class DoctorHomeView(LoginRequiredMixin, TemplateView, FormView):
    template_name = 'doctor_home.html'
    form_class = AvailabilityForm
    success_url = reverse_lazy('doctor_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch doctor from request.user
        context['doctor'] = self.request.user
        return context

    def form_valid(self, form):
        # Update doctor's availability
        availability = form.cleaned_data['availability']
        doctor_profile = self.request.user.profile
        doctor_profile.availability = availability
        doctor_profile.save()

        # Redirect to the same page on success
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class PatientManagementView(LoginRequiredMixin, ListView):
    model = Patient  # Assuming you have a Patient model
    template_name = 'patient_management.html'
    context_object_name = 'patients'

    def get_queryset(self):
        # Customize this method if you want to filter patients based on specific criteria
        return Patient.objects.all()  # Fetch all patients

    def post(self, request, *args, **kwargs):
        # Handle canceling an appointment here if needed
        patient_id = request.POST.get('patient_id')
        if patient_id:
            # Add your logic to cancel the appointment here
            patient = get_object_or_404(Patient, id=patient_id)
            patient.cancel_appointment()  # Assuming a method to cancel appointment exists
            return redirect(reverse_lazy('patient_management'))
        return super().post(request, *args, **kwargs)        
    
class PatientDetailsView(View):
    def get(self, request, patient_id):
        # Fetch the specific patient by ID
        patient = get_object_or_404(Patient, id=patient_id)
        return render(request, 'patient_details.html', {'patient': patient})  

class PatientAppointmentCancelView(View):
    def post(self, request, appointment_id):
        # Fetch the specific appointment by ID
        appointment = get_object_or_404(PatientAppointment, id=appointment_id)
        
        # Cancel the appointment (you may want to mark it as canceled instead of deleting)
        appointment.is_canceled = True  # Assuming you have an 'is_canceled' field
        appointment.save()

        messages.success(request, 'The appointment has been successfully canceled.')
        return redirect('patient_management')  # Redirect to the patient management page or wherever you want  

class CancelAppointmentConfirmationView(View):
    def get(self, request, appointment_id):
        appointment = get_object_or_404(PatientAppointment, id=appointment_id)
        return render(request, 'cancel_appointment.html', {'appointment': appointment})
    
class PatientDetailsUpdateView(View):
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        form = PatientUpdateForm(instance=patient)
        return render(request, 'patient_details_update.html', {'form': form, 'patient': patient})

    def post(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        form = PatientUpdateForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient details have been successfully updated.')
            return redirect('patient_management')  # Redirect to the patient management page or wherever you want
        return render(request, 'patient_details_update.html', {'form': form, 'patient': patient})    


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

class FacilityManagementView(ListView):
    model = Facility
    template_name = 'appointment_app/facility_management.html'  # Path to your template
    context_object_name = 'facilities'  # Name of the variable to access facilities in the template

    def get_queryset(self):
        return Facility.objects.all()  # You can add filters here if needed

class FacilityEditView(UpdateView):
    model = Facility
    form_class = FacilityForm
    template_name = 'appointment_app/facility_edit.html'
    context_object_name = 'facility'

    def get_success_url(self):
        return reverse_lazy('facility_management')  # Redirect to the facility management page after saving

    def get_object(self, queryset=None):
        return get_object_or_404(Facility, id=self.kwargs.get('facility_id'))
    

class FacilityDeleteView(DeleteView):
    model = Facility
    template_name = 'appointment_app/facility_confirm_delete.html'
    context_object_name = 'facility'
    success_url = reverse_lazy('facility_management')  # Redirect to facility management page after deletion

    def get_object(self, queryset=None):
        return get_object_or_404(Facility, id=self.kwargs.get('facility_id'))
    
class FacilityCreateView(CreateView):
    model = Facility
    form_class = FacilityForm
    template_name = 'appointment_app/facility_add.html'
    success_url = reverse_lazy('facility_management')  # Redirect to facility management page after addition

    def form_valid(self, form):
        return super().form_valid(form)    


class UserManagementView(ListView):
    template_name = 'appointment_app/user_management.html'
    context_object_name = 'users'  # You can customize this as needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()  # Fetch all patients
        context['doctors'] = Doctor.objects.all()    # Fetch all doctors
        return context
    
class UserPatientEditView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'appointment_app/patient_edit.html'
    context_object_name = 'patient'
    success_url = reverse_lazy('user_management')  # Redirect to user management page after saving

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit Patient'  # Add context for the template if needed
        return context

class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'appointment_app/patient_confirm_delete.html'  # Create this template
    success_url = reverse_lazy('user_management')  # Redirect after deletion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object  # Pass the patient object to the template
        return context
    
class DoctorEditView(UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'appointment_app/doctor_edit.html'  # Create this template
    success_url = reverse_lazy('user_management')  # Redirect after saving changes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = self.object  # Pass the doctor object to the template
        return context    
    
class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'appointment_app/doctor_confirm_delete.html'  # Create this template
    success_url = reverse_lazy('user_management')  # Redirect after deletion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = self.object  # Pass the doctor object to the template
        return context
