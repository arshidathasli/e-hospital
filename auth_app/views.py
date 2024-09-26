from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm  # Import your custom user creation form
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib import messages
from .forms import DoctorUserCreationForm  # Import your custom doctor creation form
from .forms import AdminUserCreationForm  # Import your custom admin creation form



class CustomLoginView(LoginView):
    template_name = 'login.html'  # Specify your login template

    def form_valid(self, form):
        # Call the parent class's form_valid method
        user = form.get_user()
        if user.is_superuser:
            return redirect('admin_home')  # Redirect to admin home
        elif user.role == 'doctor':
            return redirect('doctor_home')  # Redirect to doctor home
        elif user.role == 'patient':
            return redirect('patient_home')  # Redirect to patient home
        return super().form_valid(form)  # Default behavior if no role matches
    
class SignupView(CreateView):
    template_name = 'signup.html'  # Specify your template name
    form_class = CustomUserCreationForm  # Use your custom user creation form
    success_url = reverse_lazy('login')  # Redirect to login page on success

    def form_valid(self, form):
        user = form.save()  # Save the new user
        login(self.request, user)  # Log the user in immediately after signup
        messages.success(self.request, 'Signup successful!')  # Success message
        return redirect('admin_home')  # Redirect to admin home or suitable page   

class DoctorSignupView(CreateView):
    template_name = 'doctor_signup.html'  # Specify your template name
    form_class = DoctorUserCreationForm  # Use your custom doctor creation form
    success_url = reverse_lazy('login')  # Redirect to login page on success

    def form_valid(self, form):
        user = form.save()  # Save the new doctor user
        login(self.request, user)  # Log the user in immediately after signup
        messages.success(self.request, 'Doctor signup successful!')  # Success message
        return redirect('doctor_home')  # Redirect to doctor home or suitable page  

class AdminSignupView(CreateView):
    template_name = 'admin_signup.html'  # Specify your template name
    form_class = AdminUserCreationForm  # Use your custom admin creation form
    success_url = reverse_lazy('login')  # Redirect to login page on success

    def form_valid(self, form):
        user = form.save()  # Save the new admin user
        login(self.request, user)  # Log the user in immediately after signup
        messages.success(self.request, 'Admin signup successful!')  # Success message
        return redirect('admin_home')  # Redirect to admin home or suitable page


