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
        ('temp', 'Temporary'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no-show', 'No Show'),
    ]
    PAYMENT_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    MODE_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('netbanking', 'Net Banking'),
        ('upi', 'UPI'),
    ]

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments')
    department = models.CharField(max_length=100)
    appointment_date = models.CharField(max_length=20)
    appointment_time = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='temp')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='pending')
    mode_of_payment = models.CharField(max_length=50, choices=MODE_CHOICES, default='cash')

    def __str__(self):
        return f"{self.patient.first_name} with {self.doctor.first_name} on {self.appointment_date_time.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        # Ensure the patient has the 'patient' role
        if self.patient.role != 'patient':
            raise ValidationError(f'{self.patient.first_name} {self.patient.last_name} is not a valid patient.')

        # Ensure the doctor has the 'doctor' role
        if self.doctor.role != 'doctor':
            raise ValidationError(f'{self.doctor.first_name} {self.doctor.last_name} is not a valid doctor.')

    def save(self, *args, **kwargs):
        self.clean()  # Call the clean method before saving
        super().save(*args, **kwargs)


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    day = models.DateField()
    time_slots = models.JSONField()

    def __str__(self):
        return f'{self.doctor.first_name} is available on {self.day} during {self.time_slots}'


class MedicalHistory(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_medical_history')
    diagnoses = models.CharField(max_length=100, null=True, blank=True)
    allergies = models.CharField(max_length=100, null=True, blank=True)
    past_surgeries = models.CharField(max_length=100, null=True, blank=True)
    medications = models.CharField(max_length=100, null=True, blank=True)
    physical_therapy = models.CharField(max_length=100, null=True, blank=True)
    diet_plan = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.patient.first_name} with {self.doctor.first_name} on {self.date.strftime("%Y-%m-%d")}'


class Medication(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.appointment.id} on {self.start_date.strftime("%Y-%m-%d")}'


class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=100)

