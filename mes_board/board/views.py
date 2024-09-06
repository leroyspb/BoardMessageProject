from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from board.forms import MessageForm, CreateForm, CommentForm
from board.models import Message, Comment


class MessageList(LoginRequiredMixin, ListView):
    model = Message
    ordering = 'date'
    template_name = 'board_message.html'
    context_object_name = 'messages'
    paginate_by = 3


class MessageDetail(FormMixin, DetailView):
    model = Message
    template_name = 'message.html'
    context_object_name = 'message'
    queryset = Message.objects.all()
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return HttpResponse('yes')
        else:
            return HttpResponse('no')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class MessageCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('message_create',)
    raise_exception = True
    form_class = CreateForm
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




