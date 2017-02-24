from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.forms import ModelForm

class SMSMessage(models.Model):
    sender = models.ForeignKey(User, editable=False)
    recipients = models.TextField(verbose_name='Phone Numbers',
                                  validators=[RegexValidator(regex='^(\(?([2-9][0-8][0-9])\)?[-. ]?([2-9][0-9]{2})[-. ]?([0-9]{4});?)+$')],
                                 help_text='Multiple numbers should be seperated by semicolon(;)')
    msgid = models.UUIDField(editable=False)
    submit_time = models.DateTimeField(auto_now_add=True, editable=False)
    message = models.CharField(verbose_name='Message', max_length=160)

class SMSMessageForm(ModelForm):
    class Meta:
        model = SMSMessage
        fields = ['recipients', 'message']
