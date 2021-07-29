from django import forms
from django.forms import ModelForm

from webhook.base.models import Register


class RegisterForm(ModelForm):
    class Meta:
        model = Register
        widgets = {
            'date':  forms.DateInput(format='%d-%m-%Y'),
        }