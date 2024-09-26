from django import forms
from .models import Patient  # Import your Patient model
from .models import Appointment
from .models import Facility



class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'blood_group']  # List fields you want to include in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
        }
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'doctor_name', 'department', 'date_time', 'status']  # Include fields you want to edit

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'location', 'department', 'resources']  # Include the fields you want to use
