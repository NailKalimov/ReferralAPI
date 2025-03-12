from datetime import datetime
from threading import Thread

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from referrals.models import Referral


class EmailThread(Thread):
    def __init__(self, email):
        self.email = email
        Thread.__init__(self)

    def run(self):
        print(f'{self.email.send()} messages send successful')

def send_referral_code_to_email_for_current_user(user):
    active_code = Referral.objects.filter(owner=user, end_date__gte=datetime.today()).first().code
    email_addr = user.email
    if not email_addr:
        raise ObjectDoesNotExist("Empty email address")
    if not active_code:
        raise ObjectDoesNotExist("Active referral code does not found in DB")
    mail_text = f'Yor active referral code: {active_code}'
    email = EmailMessage(subject='ReferralAPI', body=mail_text, from_email="nail180@yandex.ru", to=(email_addr,))
    EmailThread(email).run()
