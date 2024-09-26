from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives

from .models import UserResponse, Message


@receiver(post_save, sender=Message)
def post_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.all().values_list('email', flat=True)
    subject = f'Новое объявление {instance.title}'
    text_content = (
        f'Добавлено новое Объявление в категории: {instance.category}\n'
        f'Ссылка на объявление: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.send()


@receiver(pre_save, sender=UserResponse)
def my_handler(sender, instance, created, **kwargs):
    if instance:
        mail = instance.author.email
        send_mail(
            'Откликнулись на Вашего героя',
            'Text Message',
            'email',
            [mail],
            fail_silently=False,
        )

    mail = instance.message.author.email
    send_mail(
        'Создан новый герой Вашего любимого автора',
        'Text Message',
        'email',
        [mail],
        fail_silently=False,
    )
