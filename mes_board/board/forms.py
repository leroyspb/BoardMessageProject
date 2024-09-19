from django import forms
from django.core.exceptions import ValidationError

from board.models import Message, UserResponse


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = [
            'author',
            'title',
            'content',
            'category',
            'message_media',

        ]

        labels = {
            'author': 'author',
            'title': 'Title',
            'content': 'Content',
            'category': ' category',

        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("description")
        title = cleaned_data.get("title")

        if title == content:
            raise ValidationError(
                "Заголовок не может быть идентичен описанию."
            )
        if content is not None and len(content) < 10:
            raise ValidationError(
                "Text: Описание не может быть менее 10 символов."
            )

        return cleaned_data


class CreateForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = [
            'title',
            'content',
            'author',
            'message_media',

        ]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        if content is not None and len(content) < 10:
            raise ValidationError(
                "Text: Описание не может быть менее 10 символов."
            )

        title = cleaned_data.get("title")
        if title == content:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class RespondForm(forms.ModelForm):

    class Meta:
        model = UserResponse
        fields = [
            'author',
            'text',

        ]

    def __init__(self, *args, **kwargs):
        super(RespondForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Описание отклика:"
