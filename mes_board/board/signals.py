from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import UserResponse
from . tasks import send_email_new_post


@receiver(pre_save, sender=UserResponse)
def my_handler(sender, instance, created, **kwargs):
    if instance:
        mail = instance.author.email
        send_mail(
            'Откликнулись на Ваше сообщение',
            'Text Message',
            'email',
            [mail],
            fail_silently=False,
        )

    mail = instance.message.author.email
    send_mail(
        'Создано новое объявление Вашего любимого автора',
        'Text Message',
        'email',
        [mail],
        fail_silently=False,
    )
