from celery import shared_task
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


def message_media(request):
    # Здесь обрабатываем файлы, загруженные пользователями
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Получаем текущий объект экземпляра для отображения в шаблоне
            cont_obj = form.instance
            return render(request,
                          'message.html',
                          {'form': form, 'cont_obj': cont_obj})
    else:
        form = MessageForm()
    return render(request,
                  'message.html',
                  {'form': form})


class MessageCreate(LoginRequiredMixin, CreateView):
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


class MessageUpdate(UpdateView):
    form_class = MessageForm
    model = Message
    template_name = 'message_edit.html'
    raise_exception = True


class MessageDelete(DeleteView):
    model = Message
    template_name = 'message_delete.html'
    success_url = reverse_lazy('message_list')
    raise_exception = True


class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = UserResponse
    template_name = 'response_delete.html'
    success_url = '/responses/'


class ResponseCreate(CreateView):
    form_class = RespondForm
    model = UserResponse
    template_name = 'response_create.html'
    success_url = '/responses/'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.author = self.request.user
        response.add_id = self.kwargs.get('pk')
        response.save()
        return super().form_valid(form)


class ResponseList(LoginRequiredMixin, ListView):
    form_class = RespondForm
    model = UserResponse
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(add__author=self.request.user)
        # Здесь применяем фильтрацию
        self.filterset = ResponseFilter(self.request.GET, queryset=queryset, request=self.request.user.id)
        return self.filterset.qs  # И возвращаем отфильтрованные результаты


def response_accept(request, **kwargs):
    if request.user.is_authenticated:
        response = UserResponse.objects.get(id=kwargs.get('pk'))
        response.status = True
        print(response.status)
        print(response)
        print(response.author)
        print(response.add_id)
        response.save()

        return HttpResponseRedirect('/responses/')
    else:
        return HttpResponseRedirect('/accounts/login')


def response_status_update(request, pk):
    if request.user.is_authenticated:
        resp = UserResponse.objects.get(pk=pk)
        resp.status = True
        resp.save()
        return HttpResponseRedirect('/responses/')
    else:
        return HttpResponseRedirect('/accounts/login')
