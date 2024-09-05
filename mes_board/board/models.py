from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Message(models.Model):
    author = models.ForeignKey(
        'auth.User',
        related_name='message_owner',
        on_delete=models.CASCADE,
        verbose_name="Owner")

    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    message_media = models.FileField(upload_to='media/', blank=True, null=True)
    related_name = 'messages',

    def __str__(self):
        return f'{self.title}: {self.content[:50]}'

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
    category = models.CharField(max_length=2, choices=CATEGORIES, default=tanks)

    def get_absolute_url(self):
        return reverse('message_detail', args=[str(self.id)])


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class Comment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()






