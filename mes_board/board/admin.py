from django import forms
from django.contrib import admin

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .forms import MessageForm
from .models import Message


class ContentAdminForm(forms.ModelForm):
    message_media = forms.CharField(label='Медиа героя', widget=CKEditorUploadingWidget())

    class Meta:
        model = Message
        fields = '__all__'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author', 'date_create')
    list_filter = ('author', 'date_create')
    form = ContentAdminForm


