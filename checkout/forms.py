from django import forms
# from django_countries.fields import CountryField
# from django_countries.widgets import CountrySelectWidget
from .models import Charge


class OrderForm(forms.ModelForm):
    class Meta:
        model = Charge
        fields = (
            'full_name', 'phone_number', 'country', 'postcode',
            'town_or_city', 'street_address1', 'street_address2'
        )
        
class PaymentForm(forms.Form):

    # use list comprhenison to generate the months and years
    MONTH_CHOICES = [(i, i) for i in range(1, 12)] # [ (1,1), (2,2), (3,3), (4,4) ... ]
    YEAR_CHOICES = [(i, i) for i in range(2020, 2036)] # [ (2020, 2020), (2021, 2021)...]

    credit_card_number = forms.CharField(label='Credit card number', required=False)
    cvv = forms.CharField(label='Security code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)
    
    