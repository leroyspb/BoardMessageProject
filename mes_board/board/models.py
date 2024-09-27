from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Message(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Создатель героя")

    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    title = models.CharField(verbose_name='Имя героя', max_length=200)
    content = models.TextField(verbose_name="Описание героя")
    message_media = models.FileField(verbose_name='Добавление медиафайлов',
                                     upload_to='media/', blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Герой'
        verbose_name_plural = 'Герои'

    tanks = 'TN'
    hills = 'HL'
    dd = 'DD'
    merchants = 'MR'
    gild_masters = 'GM'
    quest_givers = 'QG'
    blacksmiths = 'BS'
    potions_brewers = 'PB'
    spell_masters = 'SM'

    CATEGORIES = [
        (tanks, 'Танки'),
        (hills, 'Хилы'),
        (dd, 'ДД'),
        (merchants, 'Торговцы'),
        (gild_masters, 'Гилдмастеры'),
        (quest_givers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (potions_brewers, 'Зельевары'),
        (spell_masters, 'Мастера заклинаний'),

    ]
    category = models.CharField(verbose_name='Категория',
                                max_length=2,
                                choices=CATEGORIES, default=tanks)

    def get_absolute_url(self):
        """Получение абсолютного URL-адреса конкретной страницы сведений о герое."""
        return reverse('message_detail', args=[str(self.pk)])


class UserResponse(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор отклика')
    text = models.TextField(verbose_name='Текст')
    status = models.BooleanField(default=False)
    add = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, verbose_name='Мой герой')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отклика')

    def __str__(self):
        return f'{self.author}: {self.text}'

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'


class Subscription(models.Model):
    """Модель подписки на обновления"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)


