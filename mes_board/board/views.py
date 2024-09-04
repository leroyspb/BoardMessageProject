from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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


class MessageCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('message_create',)
    raise_exception = True
    form_class = MessageForm
    model = Message
    template_name = 'message_create.html'


class MessageUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_message',)
    form_class = MessageForm
    model = Message
    template_name = 'message_edit.html'


class MessageDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_message',)
    model = Message
    template_name = 'message_delete.html'
    success_url = reverse_lazy('message_list')




