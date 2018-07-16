from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .forms import MakePaymentForm, PaymentInfoForm
import stripe
from django.contrib import auth, messages
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponseRedirect
from tickets.models import Ticket, TicketType

stripe.api_key = settings.STRIPE_SECRET 

@login_required
def pay(request):
    
    if request.method=="POST":
        
        info_form = PaymentInfoForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        
        ticket = get_object_or_404(Ticket, pk=request.session.get('ticket'))
        order = get_object_or_404(TicketType, pk=request.session.get('order'))

        if info_form.is_valid() and payment_form.is_valid():
            info = info_form.save(commit=False)
            info.date_created = timezone.now()
            info.save()
            
            try:
                customer = stripe.Charge.create(
                    amount = (order.value* 100),
                    currency = 'USD',
                    description = request.user.email,
                    card = payment_form.cleaned_data['stripe_id']
                    )
                    
            except stripe.error.CardError:
                messages.error(request, "Your card was declined")
                
            if customer.paid:
                messages.success(request, "You have successfully paid")
                return redirect(reverse('pay'))
        
            else:
                messages.error(request, "Unable to take payment.")
                
        else:
            print(payment_form.errors)
            messages.error(request, "We are unable to take a payment with that card")
            
    else:
        payment_form = MakePaymentForm()
        info_form = PaymentInfoForm()
    
    return render(request, "payment.html", {'info_form':info_form, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE})
        
        