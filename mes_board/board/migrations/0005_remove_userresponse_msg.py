# Generated by Django 5.1.1 on 2024-09-26 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_alter_message_date_create_alter_message_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userresponse',
            name='msg',
        ),
    ]
