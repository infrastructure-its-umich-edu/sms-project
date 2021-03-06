from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from django_auth_ldap.backend import LDAPBackend

from .models import SMSMessageForm
from utils import twosmsutils

import logging

logger = logging.getLogger('sms.views')
messageclient = twosmsutils.twosmsMessage()


def in_allow_group(user):
    """Use with a ``user_passes_test`` decorator to restrict access to
        authenticated users who are in allowed group."""
    if user.is_authenticated():
        LDAPBackend().populate_user(user.username)
        user.refresh_from_db()
        logger.info('%s authenticated and is_staff %s' % (user, user.is_staff))
        if not user.is_staff:
            raise PermissionDenied
    return True


@login_required
@user_passes_test(in_allow_group)
def get_message(request):
    if request.method == 'POST':
        form = SMSMessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.message = new_message.message + " -"
            + request.user.username
            new_message.sender = request.user
            new_message.submit_time = timezone.now()
            result = messageclient.send(new_message)
            if int(result.Code) == 0:
                new_message.save()
                logger.info(result.ResultText)
                messages.success(request, result.ResultText)
                return HttpResponseRedirect('')
            else:
                logger.error(result.SendResult)
                messages.error(request, result.ResultText)

    else:
        form = SMSMessageForm()
        form.fields['message'].widget.attrs['maxlength'] = 150
        form.fields['recipients'].widget.attrs['rows'] = 1

    return render(request, 'sendsms/message.html', {'form': form})
