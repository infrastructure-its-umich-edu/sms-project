from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.conf import settings
from django_auth_ldap.backend import LDAPBackend
from kitchen.text.converters import to_bytes

from .forms import MessageForm
from utils import twosmsutils

import logging

logger = logging.getLogger(__name__)
messageclient = twosmsutils.twosmsMessage()
allow_group = settings.ALLOW_GROUP

def in_allow_group(user):
    if user.is_authenticated():
        LDAPBackend().get_all_permissions(user)
    """Use with a ``user_passes_test`` decorator to restrict access to
        authenticated users who are in allowed group."""
    return user.groups.filter(name=allow_group).exists()

@login_required
@user_passes_test(in_allow_group, login_url='/accounts/test/')
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
            logger.info(result)
            return HttpResponse("Result: %s" % result )

    else:
        form = MessageForm()

    return render(request, 'sendsms/message.html', {'form': form})
