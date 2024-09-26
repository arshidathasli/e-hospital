from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Import your custom user model
from .models import Doctor
from .models import Admin

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  # Include your fields here

class DoctorUserCreationForm(UserCreationForm):
    class Meta:
        model = Doctor  # Use your custom Doctor model
        fields = ['username', 'email', 'specialization', 'password1', 'password2']  # Include relevant fields

class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = Admin  # Use your custom Admin model
        fields = ['username', 'email', 'password1', 'password2']        