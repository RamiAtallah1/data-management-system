from django.core.mail import send_mail
from django.conf import settings


def send_import_confirmation(title, message, email):
    send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=True,
    )
