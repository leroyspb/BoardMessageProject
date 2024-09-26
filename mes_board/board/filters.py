import django_filters
from django import forms
from .models import Message, UserResponse


class MessageFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Имя героя'
    )

    category = django_filters.ChoiceFilter(
        choices=Message.CATEGORIES,
        label='Категория героя',
        empty_label='Выберите категорию',
    )

    created_at_after = django_filters.DateTimeFilter(
        field_name='date_create',
        lookup_expr='gt',
        label='Дата создания героя',
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Message  # Модель для фильтрации
        fields = ['title', 'category', 'created_at_after']


class ResponseFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['add'].queryset = Message.objects.filter(author_id=kwargs['request'])

    class Meta:
        model = UserResponse
        fields = ('add', )
