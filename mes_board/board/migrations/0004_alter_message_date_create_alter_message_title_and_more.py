# Generated by Django 5.1.1 on 2024-09-26 17:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_alter_message_options_alter_message_content_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='message',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Имя героя'),
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='add',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='board.message', verbose_name='Мой герой'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userresponse',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор отклика'),
        ),
    ]
