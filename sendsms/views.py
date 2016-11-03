from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import MessageForm

def get_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # do something like send the message
            # then redirect to acknowledgement url
            return HttpResponseRedirect('/sms/send')

    else:
        form = MessageForm()

    return render(request, 'sendsms/message.html', {'form': form})
