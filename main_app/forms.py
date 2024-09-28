from django import forms
from auth_app.models import CustomUser  # Import your CustomUser model
from .models import Appointment, Facility  # Import models from the same app

class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Use your custom user model
        fields = ['first_name', 'last_name', 'age', 'gender', 'blood_group']  # Specify existing fields in your model
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment  # Use your Appointment model
        fields = ['patient', 'doctor', 'department', 'appointment_date_time', 'status']  # Specify the fields
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'appointment_date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
