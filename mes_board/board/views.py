from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic import ListView

from board.models import Message


class MessageList(ListView):
    model = Message
    ordering = 'author'
    template_name = 'board_message.html'
    context_object_name = 'messages'


def profile_view(request):
    return render(request, 'registration/login.html')

