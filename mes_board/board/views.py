from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from board.filters import MessageFilter, ResponseFilter
from board.forms import MessageForm, CreateForm, RespondForm
from board.models import Message, UserResponse
from .tasks import respond_send_email, respond_accept_send_email


class MessageList(ListView):
    model = Message
    ordering = '-date_create'
    template_name = 'board_message.html'
    context_object_name = 'messages'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        # Здесь применяем фильтрацию
        self.filterset = MessageFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs  # И возвращаем отфильтрованные результаты

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class IndexView(ListView):
    model = Message
    template_name = 'index.html'
    context_object_name = 'messages'


class MessageDetail(DetailView):
    model = Message
    template_name = 'message.html'
    context_object_name = 'messages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message_id = self.kwargs.get('pk')
        context['respond'] = "Откликнулся" if UserResponse.objects.filter(
            author=self.request.user,
            id=message_id) else "Мое_объявление" \
            if self.request.user == self.get_object().author else None

        return context


def image_upload_view(request):
    # Здесь обрабатываем файлы, загруженные пользователями
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Получаем текущий объект экземпляра для отображения в шаблоне
            cont_obj = form.instance
            return render(request,
                          'index.html',
                          {'form': form, 'cont_obj': cont_obj})
    else:
        form = MessageForm()
    return render(request,
                  'index.html',
                  {'form': form})


class MessageCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('board.add_message',)
    raise_exception = True
    form_class = CreateForm
    model = Message
    template_name = 'message_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Устанавливаем автора
        return super().form_valid(form)

    def add_message(request):
        if not request.user.has_perm('board.add_message'):
            raise PermissionDenied

    def get_success_url(self):
        return reverse('message_list')


class MessageUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('board.change_message',)
    form_class = MessageForm
    model = Message
    template_name = 'message_edit.html'
    raise_exception = True


class MessageDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('board.delete_message',)
    model = Message
    template_name = 'message_delete.html'
    success_url = reverse_lazy('message_list')
    raise_exception = True


class CommentDetail(DetailView):
    model = UserResponse
    template_name = 'comment_detail.html'
    context_object_name = 'comment'


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = UserResponse
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('message')


class CommentEdit(LoginRequiredMixin, UpdateView):
    model = UserResponse
    template_name = 'comment_edit.html'
    success_url = reverse_lazy('message')


class AddComment(PermissionRequiredMixin, CreateView):
    model = UserResponse
    template_name = 'add_comment.html'
    success_url = reverse_lazy('message')


class ResponseList(LoginRequiredMixin, ListView):
    form_class = RespondForm
    model = UserResponse
    template_name = 'responses.html'
    context_object_name = 'responses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(message__author=self.request.user)
        self.filterset = ResponseFilter(self.request.GET, queryset, request=self.request.user.id)
        return self.filterset.qs


def response_accept(request, **kwargs):
    if request.user.is_authenticated:
        response = UserResponse.objects.get(id=kwargs.get('pk'))
        response.status = True
        response.save()
        respond_accept_send_email.delay(response_id=response.id)
        return HttpResponseRedirect('/responses')
    else:
        return HttpResponseRedirect('/accounts/login')


def response_delete(request, **kwargs):
    if request.user.is_authenticated:
        response = UserResponse.objects.get(id=kwargs.get('pk'))
        response.delete()
        return HttpResponseRedirect('/responses')
    else:
        return HttpResponseRedirect('/accounts/login')


class AcceptResponseView(LoginRequiredMixin, View):
    def post(self, request, pk):
        application = get_object_or_404(UserResponse, id=pk)
        application.accepted = True
        application.save()

        # Уведомление пользователя, который оставил отклик
        send_notification(application.user, application)

        messages.success(request, "Отклик принят.")
        return redirect('applications_list')


def send_notification(user, application):
    # Реализация уведомления
    pass

