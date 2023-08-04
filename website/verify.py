import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(os.environ['TWILIO_ACCOUNT_SID'],
                os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])


def send(phone):
    phone_number = str(phone.as_e164)
    verify.verifications.create(to=phone_number, channel='sms')


def check(phone, code):
    phone_number = str(phone.as_e164)
    try:
        result = verify.verification_checks.create(to=phone_number, code=code)
        print('validated')
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'
