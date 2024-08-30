import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from board.models import Message
from mes_board import settings


@shared_task
def send_email_new_post(pk):
    message = Message.objects.get(pk=pk)
    title = message.title
    subscribers = []
    for aut in authors:
        subscribers_users = category.subscribers.all()
        for sub_user in subscribers_users:
            subscribers.append(sub_user.email)

    html_content = render_to_string(
        'message_created_email.html',
        {
            'text': f'{message.title}',
            'link': f'{settings.SITE_URL}{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject='Появилась новая новость',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def weekly_email_task(pk):
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(creation_time_in__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    print(subscribers)
    html_content = render_to_string(
        'news/daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()
