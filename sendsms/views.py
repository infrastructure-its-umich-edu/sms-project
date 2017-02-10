from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib import messages
from django_auth_ldap.backend import LDAPBackend
from kitchen.text.converters import to_bytes

from .forms import MessageForm
from utils import twosmsutils

import logging

logger = logging.getLogger('sms.views')
messageclient = twosmsutils.twosmsMessage()

def in_allow_group(user):
    """Use with a ``user_passes_test`` decorator to restrict access to
        authenticated users who are in allowed group."""
    if user.is_authenticated():
        logger.debug('in_allow_group %s is authenticated' % user)
        LDAPBackend().populate_user(user.username)
        if not user.is_staff:
            raise PermissionDenied
    return True

@login_required
@user_passes_test(in_allow_group)
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
            logger.info(result.ResultText)
            if int(result.Code) == 0:
                messages.success(request, result.ResultText)
            else:
                messages.error(request, result.ResultText)

    else:
        form = MessageForm()

    return render(request, 'sendsms/message.html', {'form': form})
