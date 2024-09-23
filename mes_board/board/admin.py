from django.contrib import admin
from django.contrib.gis import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .forms import MessageForm
from .models import Message


class ContentAdminForm(forms.ModelForm):
    message_media = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Message
        fields = '__all__'


class MessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author', 'date_create']
    list_filter = ('author', 'date_create')
    form = ContentAdminForm


admin.site.register(Message, MessageAdmin, ContentAdminForm)

