from django import forms
from Payment_app.models import Billing_address


class Billing_form(forms.ModelForm):
    class Meta:
        model = Billing_address
        fields = ['address', 'zipcode', 'city', 'country']