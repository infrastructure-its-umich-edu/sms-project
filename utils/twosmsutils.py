from django.conf import settings
from zeep import Client
from zeep import xsd
from zeep.cache import InMemoryCache
from zeep.transports import Transport
import uuid

def msgTypeList(numbs):
    list = '2'
    for num in range(numbs):
        list = list + ';2'
    return list

class twosmsMessage:
    """A utility class for connecting with sms vendor 2sms"""
    sms_user = settings.SMS_USER
    sms_pass = settings.SMS_PASS
    mc = Client('https://smsportal.2sms.com/WebServices/2.2/Simple/Message.asmx?WSDL',
               transport=Transport(cache=InMemoryCache()))
    messageClient = mc.bind('Message', 'MessageSoap12')

    def send(self, to, message):
        msgid = str(uuid.uuid1())
        msgtypes = msgTypeList(to.count(';'))
        return self.messageClient.Send(self.sms_user,
                                       self.sms_pass,
                                       msgtypes,
                                       msgtypes.replace('2','1'),
                                       to,
                                       message,
                                       'NULL',
                                       'header',
                                       msgid,
                                       'NULL',
                                       '1',
                                       '1',
                                       '1',
                                       'result',
                                       'code')
