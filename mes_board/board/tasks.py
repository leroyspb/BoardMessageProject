import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from celery import shared_task
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from board.models import Message, UserResponse
from mes_board import settings


@shared_task
def respond_send_email(respond_id):
    respond = UserResponse.objects.get(id=respond_id)
    send_mail(
        subject=f'Герои MMORPG : новый отклик на твоего героя!',
        message=f'Доброго дня, {respond.message.author}, ! Вашему герою присвоен новый отклик!\n'
                f'Прочитать отклик:\nhttp://127.0.0.1:8000/responses/{respond.message.id}',
        from_email='leroyspb@ya.ru',
        recipient_list=[respond.message.author.email, ],
    )

    html_content = render_to_string(
        'message_created_email.html',
        {
            'text': f'{Message.title}',
            'link': f'{settings.SITE_URL}{respond.message.id}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Появился новый герой',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=respond.message.author,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def send_mail_monday_8am():
    # Здесь формируем список всех героев, созданных за последние 7 дней (list_week_messages)
    now = timezone.now()
    list_week_messages = list(Message.objects.filter(
        date_create__gte=now - datetime.timedelta(days=7)))
    if list_week_messages:
        for user in User.objects.filter():
            print(user)
            list_messages = ''
            for message in list_week_messages:
                list_messages += f'\n{message.title}\nhttp://127.0.0.1:8000/{message.id}'
            send_mail(
                subject=f'MMORPG Герои: изменения за прошедшую неделю.',
                message=f'Доброго дня, {user.username}!\nПредлагаем Вам ознакомиться с новыми объявлениями, '
                        f'появившимися за последние 7 дней:\n{list_messages}',
                from_email='leroyspb@ya.ru',
                recipient_list=[user.email, ],
            )


@shared_task
def respond_accept_send_email(response_id):
    respond = UserResponse.objects.get(id=response_id)
    print(respond.message.author.email)
    send_mail(
        subject=f'MMORPG Герои: Ваш отклик принят!',
        message=f'Доброго дня, {respond.author}, Автор героя {respond.message.title} принял Ваш отклик!\n'
                f'Посмотреть принятые отклики:\nhttp://127.0.0.1:8000/responses',
        from_email='leroyspb@ya.ru',
        recipient_list=[respond.message.author.email, ],
    )
