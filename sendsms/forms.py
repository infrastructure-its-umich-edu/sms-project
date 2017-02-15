from django import forms
from django.core.validators import RegexValidator


class MessageForm(forms.Form):
    number = forms.CharField(label='Phone Number',
                             validators=[RegexValidator(regex='^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4});?)+$')])
    message = forms.CharField(label='Message', max_length=160)
