from django.contrib import admin
from django.urls import path
from auth_app.views import (
    CustomLoginView,
    SignUpView,
    LogoutView,
)
from main_app.views import (
    # Patient related
    PatientHomeView,
    PatientMedicalHistoryView,
    DoctorsListView,
    AppointmentTimeView,
    # Doctor related
    DoctorHomeView,
    DoctorProfileView,
    PatientManagementView,
    DoctorAvailabilityView,


    # PatientDetailsView,
    # PatientAppointmentCancelView,
    # CancelAppointmentConfirmationView,
    # PatientDetailsUpdateView,
    # EPrescribingView,
    # AdminHomeView,
    # AdminAppointmentManagementView,
    # AppointmentEditView,
    # AppointmentCancelView,
    # AppointmentCreateView,
    # FacilityManagementView,
    # FacilityEditView,
    # FacilityDeleteView,
    # FacilityCreateView,
    # UserManagementView,
    # UserPatientEditView,
    # PatientDeleteView,
    # DoctorEditView,
    # DoctorDeleteView
)
from main_app.views import update_profile

# from payment_app.views import (
#     ProceedPaymentView,
#     PaymentView,
#     ProcessPaymentView,
#     PaymentSuccessView,
# )

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth app
    path('', CustomLoginView.as_view(), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    # path('doctor_signup/', DoctorSignupView.as_view(), name='doctor_signup'),
    # path('admin_signup/', AdminSignupView.as_view(), name='admin_signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Patient paths
    path('patient_home/', PatientHomeView.as_view(), name='patient_home'),
    path('patient_medical_history/', PatientMedicalHistoryView.as_view(), name='patient_medical_history'),
    path('doctors_list/', DoctorsListView.as_view(), name='doctors_list'),
    path('appointment_time/', AppointmentTimeView.as_view(), name='appointment_time'),
    # path('proceed_payment/', ProceedPaymentView.as_view(), name='proceed_payment'),
    # path('payment/', PaymentView.as_view(), name='payment_signup'),
    # path('process_payment/', ProcessPaymentView.as_view(), name='process_payment'),
    # path('payment_success/', PaymentSuccessView.as_view(), name='payment_success'),

    # Doctor paths
    path('doctor_home/', DoctorHomeView.as_view(), name='doctor_home'),
    path('doctor_profile/', DoctorProfileView.as_view(), name='doctor_profile'),
    path('patient_management/', PatientManagementView.as_view(), name='patient_management'),
    path('doctor_availablity/', DoctorAvailabilityView.as_view(), name='doctor_availability'),
    path('update-profile/', update_profile, name='update_profile'),

    # path('patient_details/<int:patient_id>/', PatientDetailsView.as_view(), name='patient_details'),
    # path('patient_appointment_cancel/<int:appointment_id>/', PatientAppointmentCancelView.as_view(), name='patient_appointment_cancel'),
    # path('cancel_appointment/<int:appointment_id>/', CancelAppointmentConfirmationView.as_view(), name='cancel_appointment'),
    # path('patient_details_update/<int:patient_id>/', PatientDetailsUpdateView.as_view(), name='patient_details_update'),
    # path('E-prescribing/', EPrescribingView.as_view(), name='E-prescribing'),

    # Admin paths
    # path('admin_home/', AdminHomeView.as_view(), name='admin_home'),
    # path('admin_appointment_management/', AdminAppointmentManagementView.as_view(), name='admin_appointment_management'),
    # path('appointment_edit/<int:pk>/', AppointmentEditView.as_view(), name='appointment_edit'),
    # path('appointment_cancel/', AppointmentCancelView.as_view(), name='appointment_cancel'),
    # path('appointment/add/', AppointmentCreateView.as_view(), name='appointment_add'),
    # path('facility_management/', FacilityManagementView.as_view(), name='facility_management'),
    # path('edit_facility/<int:facility_id>/', FacilityEditView.as_view(), name='facility_edit'),
    # path('delete_facility/<int:facility_id>/', FacilityDeleteView.as_view(), name='facility_delete'),
    # path('add_facility/', FacilityCreateView.as_view(), name='facility_add'),
    # path('user_management/', UserManagementView.as_view(), name='user_management'),
    # path('edit_patient/<int:pk>/', UserPatientEditView.as_view(), name='edit_patient'),
    # path('patient_delete/<int:pk>/', PatientDeleteView.as_view(), name='patient_delete'),
    # path('doctor_edit/<int:pk>/', DoctorEditView.as_view(), name='doctor_edit_view'),
    # path('doctor_delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete_view'),
]
