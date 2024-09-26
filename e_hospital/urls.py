from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth app
    # path('', CustomLoginView.as_view(), name='login'),  # Use your custom LoginView
    # path('signup/', signup.as_view, name='signup'), 
    # path('doctor_signup/', doctor_signup.as_view, name='doctor_signup'),  
    # path('admin_signup/', signup.as_view, name='admin_signup'),

    # #patient
    # path('patient_home/', patient_home.as_view, name='patient_home'),
    # path('doctors_list/', doctors_list.as_view, name='doctors_list'),
    # path('take_appointment/', take_appointment_view, name='take_appointment'),
    # path('appointment_time/', appointment_time.as_view, name='appointment_time'),
    # path('proceed_payment/', proceed_payment.as_view, name='proceed_payment'),
    # path('payment/', PaymentView.as_view(), name='payment_signup'),
    # path('process_payment/', ProcessPaymentView.as_view(), name='process_payment'),
    # path('payment_success/', PaymentSuccessView.as_view(), name='payment_success'),

    # #doctor
    # path('doctor_home/', DoctorHomeView.as_view(), name='doctor_home'),
    # path('doctor_availability_update/', doctor_availability_update.as_view, name='doctor_availability_update'),
    # path('patient_management/', PatientManagementView.as_view(), name='patient_management'),
    # path('patient_details/<int:patient_id>/', PatientDetailsView.as_view(), name='patient_details'),
    # path('patient_appointment_cancel/<int:appointment_id>/', PatientAppointmentCancelView.as_view(), name='patient_appointment_cancel'),
    # path('cancel_appointment/<int:appointment_id>/', CancelAppointmentConfirmationView.as_view(), name='cancel_appointment'),
    # path('patient_details_update/<int:patient_id>/', PatientDetailsUpdateView.as_view(), name='patient_details_update'),
    # path('E-prescribing/', EPrescribingView.as_view(), name='E-prescribing'),

    # #admin
    # path('admin_home/', AdminHomeView.as_view(), name='admin_home'),
    # path('admin_appointment_management/', AdminAppointmentManagementView.as_view(), name='admin_appointment_management'),  # Use .as_view() for class-based views
    # path('appointment_edit/<int:pk>/', AppointmentEditView.as_view(), name='appointment_edit'),  # Include the appointment ID as a parameter
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
