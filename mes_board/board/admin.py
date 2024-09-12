from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author', 'date_create']
    list_filter = ('author', 'date_create')


admin.site.register(Message, MessageAdmin)
