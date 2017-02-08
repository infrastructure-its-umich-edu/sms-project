from django.conf import settings
from zeep import Client
from zeep import xsd
import uuid

class twosmsMessage:
    """A utility class for connecting with sms vendor 2sms"""
    sms_user = settings.SMS_USER
    sms_pass = settings.SMS_PASS
    mc = Client('https://smsportal.2sms.com/WebServices/2.2/Simple/Message.asmx?WSDL')
    messageClient = mc.bind('Message', 'MessageSoap12')

    def send(self, to, message):
        msgid = str(uuid.uuid1())
        return self.messageClient.Send( self.sms_user, self.sms_pass, '2', '1', to, message, 'NULL', 'header', msgid, 'NULL', '1', '1', '1', 'result', 'code' )
