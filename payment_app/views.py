from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app.models import Appointment



class CashPaymentView(LoginRequiredMixin, View):
    template_name = 'appointment_booked.html'
    
    def get(self, request, appointment_id):
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = 'scheduled'
        appointment.save()
        context = {
            'appointment_id': appointment_id,
        }
        return render(request, self.template_name, context)


# Payment View (handles the form submission for payment)
class PaymentView(FormView):
    template_name = 'payment.html'
    success_url = reverse_lazy('payment_success')  # URL to redirect to after payment

    def form_valid(self, form):
        # Process the payment here (e.g., integrate with a payment gateway)
        # You can also access form data with `form.cleaned_data`

        # Assuming payment is successful, we redirect to the success page
        return super().form_valid(form)



# Class-based view to handle payment processing
class ProcessPaymentView(View):
    def post(self, request, *args, **kwargs):
        # Get form data
        name_on_card = request.POST.get('nameOnCard')
        card_number = request.POST.get('cardNumber')
        exp_date = request.POST.get('expDate')
        cvv = request.POST.get('cvv')
        amount = request.POST.get('amount')

        # Here you would typically process the payment using a payment gateway API
        # For simplicity, we assume the payment is always successful

        # Example: If payment is successful, redirect to success page
        return redirect('payment_success')

# Success view
class PaymentSuccessView(TemplateView):
    template_name = 'payment_success.html'

