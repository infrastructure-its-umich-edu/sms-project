from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect

from .forms import MessageForm
from utils import twosmsutils

import logging

logger = logging.getLogger(__name__)
messageclient = twosmsutils.twosmsMessage()

@login_required
def get_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            clean_number = form.cleaned_data['number']
            clean_message = form.cleaned_data['message']
            # do something like send the message
            # then redirect to acknowledgement url
            result = messageclient.send( clean_number, clean_message )
            logger.debug(result)
            return HttpResponseRedirect('/sms/send')

    else:
        form = MessageForm()

    return render(request, 'sendsms/message.html', {'form': form})
