from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Doctor(models.Model):
    user = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    
    def __str__(self):
        return f'Dr. {self.user.first_name} {self.user.last_name} - {self.specialty}'
    
    def clean(self):
        if self.user.role != 'doctor':
            raise ValidationError(f'{self.user.first_name} {self.user.last_name} is not assigned the doctor role.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no-show', 'No Show'),
    ]

    patient = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='patient_appointment')
    doctor = models.ForeignKey('auth_app.CustomUser', on_delete=models.CASCADE, related_name='doctor_appointment')
    department = models.CharField(max_length=100)
    appointment_date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"{self.patient.first_name} - {self.doctor.first_name} on {self.appointment_date_time.strftime('%Y-%m-%d %H:%M')}"
    
    def clean(self):
        if self.patient.role != 'patient':
            raise ValidationError(f'{self.patient.first_name} {self.patient.last_name} is not a valid patient.')

        if self.doctor.role != 'doctor':
            raise ValidationError(f'Dr. {self.doctor.first_name} {self.doctor.last_name} is not a valid doctor.')

        if self.appointment_date_time < timezone.now():
            raise ValidationError('The appointment date and time cannot be in the past.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
