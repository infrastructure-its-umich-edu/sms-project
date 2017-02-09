from django import forms
from django.core.validators import RegexValidator


class MessageForm(forms.Form):
    number = forms.CharField(label='Phone Number',
                             validators=[RegexValidator(regex='^[0-9]{10}$')])
    message = forms.CharField(label='Message', max_length=160)
