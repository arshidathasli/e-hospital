from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from auth_app.models import CustomUser  # Adjust the import based on your project structure

class Specialization(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use the imported CustomUser directly
    specialization = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50, null=True, blank=True)
    fee = models.PositiveIntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return f'Dr. {self.user.email} - {self.specialization}'

    def clean(self):
        # Ensure the user has the 'doctor' role
        if self.user.role != 'doctor':
            raise ValidationError(f'{self.user.email} is not assigned the doctor role.')

    def save(self, *args, **kwargs):
        self.clean()  # Call the clean method before saving
        super().save(*args, **kwargs)


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no-show', 'No Show'),
    ]

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments')
    department = models.CharField(max_length=100)
    appointment_date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"{self.patient.first_name} with {self.doctor.first_name} on {self.appointment_date_time.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        # Ensure the patient has the 'patient' role
        if self.patient.role != 'patient':
            raise ValidationError(f'{self.patient.first_name} {self.patient.last_name} is not a valid patient.')

        # Ensure the doctor has the 'doctor' role
        if self.doctor.role != 'doctor':
            raise ValidationError(f'{self.doctor.first_name} {self.doctor.last_name} is not a valid doctor.')

        # Check if the appointment date and time is in the past
        if self.appointment_date_time < timezone.now():
            raise ValidationError('The appointment date and time cannot be in the past.')

    def save(self, *args, **kwargs):
        self.clean()  # Call the clean method before saving
        super().save(*args, **kwargs)


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    day = models.DateField()
    time_slots = models.JSONField()

    def __str__(self):
        return f'{self.doctor.first_name} is available on {self.day} during {self.time_slots}'

