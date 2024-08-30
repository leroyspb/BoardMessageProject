from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from board.forms import MessageForm
from board.models import Message


class MessageList(LoginRequiredMixin, ListView):
    model = Message
    ordering = 'date'
    template_name = 'board_message.html'
    context_object_name = 'messages'
    paginate_by = 3


class MessageDetail(DetailView):
    model = Message
    template_name = 'message.html'
    context_object_name = 'message'
    queryset = Message.objects.all()


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('message_create',)
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = MessageForm

    # модель
    model = Message
    # и новый шаблон, в котором используется форма.
    template_name = 'message_create.html'





