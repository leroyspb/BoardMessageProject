from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import redirect
from django.urls import reverse

from board.models import UserResponse


@receiver(post_save, sender=UserResponse)
def send_mail_on_response(sender, instance, created, **kwargs):

    """
Отправляем электронные письма о новом отклике автору героя и юзерам.
    sender: Класс модели отклика, который вызвал этот сигнал.
    instance: Фактический экземпляр модели UserResponse, который был сохранен.
    created: логическое значение, указывающее, был ли создан новый экземпляр (True) или обновлен существующий экземпляр (False).
    kwargs: Дополнительные аргументы ключевого слова, передаваемые обработчику сигнала.
    """

    responder = instance.author
    add = instance.add
    if created:
        subject = 'Получен новый отклик!'
        text = f'{add.author.username}, кто-то откликнулся на Вашего героя'
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[add.author.email]
        )
        responses_link = redirect('response')
        # responses_link = reverse('response')
        html = (
            f'<b>{responder.username}</b> откликнулся на объявление "{add.title}".'
            f'Принять или удалить отклик Вы можете по <a href="{responses_link}">ссылке</a>.'
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        subject = 'Отклик отправлен!'
        text = (f'{responder.username}, Вы оставили отклик на героя "{add.title}". '
                      f'Когда автор героя примет решение по Вашему отклику, Вы получите письмо о статусе отклика.')
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[responder.email]
        )
        msg.send()

    if instance.status:
        subject = 'Отклик принят!'
        text = f'Поздравляем! Ваш отклик на объявление "{add.title}" был принят!'
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[responder.email]
        )
        msg.send()
