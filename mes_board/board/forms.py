from django import forms
from django.core.exceptions import ValidationError

from board.models import Message


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = [
            'author',
            'title',
            'content',

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


