from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,HttpResponseRedirect
from kitchen.text.converters import to_bytes

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
            clean_number = form.cleaned_data.get('number')
            clean_message = form.cleaned_data.get('message')
            # do something like send the message
            # then redirect to acknowledgement url
            result = messageclient.send( to_bytes(clean_number, encoding='ascii' ),
                                         to_bytes(clean_message, encoding='ascii' ))
            logger.debug(result)
            return HttpResponse("Result: %s" % result )

    else:
        form = MessageForm()

    return render(request, 'sendsms/message.html', {'form': form})
