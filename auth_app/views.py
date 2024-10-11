from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm


class CustomLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'patient':
                return redirect('patient_home')
            elif user.role == 'doctor':
                return redirect('doctor_home')
            elif user.role == 'admin':
                return redirect('admin_home')
            else:
                return redirect('patient_home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')


class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data.get('role')
            user.save()
            login(request, user)
            messages.success(request, 'Patient signup successful!')
            if user.role:
                return redirect('admin_home')
            elif user.role == 'doctor':
                return redirect('doctor_home')
            elif user.role == 'patient':
                return redirect('patient_home')
            else:
                return redirect('patient_home')
        else:
            return render(request, 'signup.html', {'form': form})
        

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


