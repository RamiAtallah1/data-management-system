from django.core.mail import send_mail


def send_import_confirmation(title, message, email):
    send_mail(
        title,
        message,
        "ramiatallah722@gmail.com",
        [email],
        fail_silently=True,
    )
