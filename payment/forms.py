from django import forms
from .models import PaymentInfo

class MakePaymentForm(forms.Form):
    
    MONTH_CHOICES = [(i, i) for i in range(1,12)]
    YEAR_CHOICES = [(i, i) for i in range(2018, 2037)]
    
    credit_card_number = forms.CharField(label='Credit Card Number', required='False')
    cvv = forms.CharField(label='Security Code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES, required=False)
    stripe=id = forms.CharField(widget=forms.HiddenInput)

class PaymentInfoForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        fields = ('full_name','phone_number','street_address1', 'street_address2', 'city','county', 'country', 'postcode', )

