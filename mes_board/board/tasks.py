import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from celery import shared_task

from django.core.mail import send_mail

from board.models import Message


@shared_task
def send_mail_monday_8am(pk):
    print('GOOD')
    # Здесь формируем список всех героев, созданных за последние 7 дней (list_week_messages)
    now = timezone.now()
    list_week_messages = list(Message.objects.filter(
        date_create__gte=now - datetime.timedelta(days=7)))
    if list_week_messages:
        for user in User.objects.filter():
            list_messages = ''
            for message in list_week_messages:
                list_messages += f'\n{message.title}\nhttp://127.0.0.1:8000/{message.id}'
            send_mail(
                subject=f'MMORPG Герои: изменения за прошедшую неделю.',
                message=f'Доброго дня, {user.username}!\nПредлагаем Вам ознакомиться с новыми, '
                        f'появившимися за последние 7 дней героями:\n{list_messages}',
                from_email='leroyspb@ya.ru',
                recipient_list=[user.email, ],
            )


