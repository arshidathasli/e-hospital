from django.contrib import admin
from django.urls import path
from auth_app.views import (
    CustomLoginView,
    SignUpView,
    LogoutView,
)
from payment_app.views import (
    CashPaymentView,

    # ProceedPaymentView,
    # PaymentView,
    # ProcessPaymentView,
    # PaymentSuccessView,
)

from main_app.views import (
    # Patient related
    PatientHomeView,
    PatientProfileView,
    PatientMedicalHistoryView,
    PatientAppointmentHistoryView,
    DoctorsListView,
    AppointmentTimeView,
    ViewPrescriptionView,
    ViewResourcesView,

    # Doctor related
    DoctorHomeView,
    DoctorProfileView,
    PatientManagementView,
    DoctorAvailabilityView,
    ConfirmAppointmentView,
    ViewAppointmentView,
    PrescribeView,

    #Functions
    update_profile,
    update_doctor_availability,
    cancel_appointment,
    add_medication,
    remove_medication,
    save_prescription,

    # Admin related
    AdminHomeView,
    AdminProfileView,
    AdminDoctorsListView,
    AdminPatientsListView,
    AdminAppointmentsListView,

    # Admin functions
    admin_update_profile,
)


urlpatterns = [
    # Admin paths
    path('admin_home/', AdminHomeView.as_view(), name='admin_home'),
    path('admin_profile/', AdminProfileView.as_view(), name='admin_profile'),
    path('admin_doctors_list/', AdminDoctorsListView.as_view(), name='admin_doctors_list'),
    path('admin_patients_list/', AdminPatientsListView.as_view(), name='admin_patients_list'),
    path('admin_appointments_list/', AdminAppointmentsListView.as_view(), name='admin_appointments_list'),
    path('admin_update_profile/', admin_update_profile, name='admin_update_profile'),
    path('cancel_appointment/', cancel_appointment, name='cancel_appointment_by_admin'),

    path('admin/', admin.site.urls),

    # Auth app
    path('', CustomLoginView.as_view(), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Patient paths
    path('patient_home/', PatientHomeView.as_view(), name='patient_home'),
    path('patient_profile/', PatientProfileView.as_view(), name='patient_profile'),
    path('view_resources/', ViewResourcesView.as_view(), name='view_resources'),
    path('patient_medical_history/', PatientMedicalHistoryView.as_view(), name='patient_medical_history'),
    path('patient_appointment_history/', PatientAppointmentHistoryView.as_view(), name='patient_appointment_history'),
    path('patient_medical_history/cancel_appointment/', cancel_appointment, name='cancel_appointment_by_patient'),
    path('doctors_list/', DoctorsListView.as_view(), name='doctors_list'),
    path('appointment_time/', AppointmentTimeView.as_view(), name='appointment_time'),
    path('confirm-appointment/', ConfirmAppointmentView.as_view(), name='confirm_appointment'),
    path('confirm-appointment/cash-payment/<int:appointment_id>/', CashPaymentView.as_view(), name='cash_payment_url'),
    path('view_prescription/<int:id>/', ViewPrescriptionView.as_view(), name='view_prescription'),

    # Doctor paths
    path('doctor_home/', DoctorHomeView.as_view(), name='doctor_home'),
    path('doctor_profile/', DoctorProfileView.as_view(), name='doctor_profile'),
    path('patient_management/', PatientManagementView.as_view(), name='patient_management'),
    path('doctor_availablity/', DoctorAvailabilityView.as_view(), name='doctor_availability'),
    path('update-profile/', update_profile, name='update_profile'),
    path('update-doctor-availability/', update_doctor_availability, name='update_doctor_availability'),
    path('patient_management/cancel_appointment/', cancel_appointment, name='cancel_appointment_by_doctor'),
    path('patient_management/view_appointment/', ViewAppointmentView.as_view(), name='view_appointment_by_doctor'),
    path('patient_management/view_appointment/e_prescribing/', PrescribeView.as_view(), name='prescribe'),
    path('add_medication/', add_medication, name='add_medication'),
    path('remove_medication/', remove_medication, name='remove_medication'),
    path('save_prescription/', save_prescription, name='save_prescription'),

]
