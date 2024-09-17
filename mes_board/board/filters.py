import django_filters
from django import forms
from .models import Message


class MessageFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок'
    )

    category = django_filters.ChoiceFilter(
        choices=Message.CATEGORIES,
        label='Категории',
        empty_label='Выберите категорию',
    )

    created_at_after = django_filters.DateTimeFilter(
        field_name='date_create',
        lookup_expr='gt',
        label='Дата',
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Message  # Модель для фильтрации
        fields = ['title', 'category', 'created_at_after']

