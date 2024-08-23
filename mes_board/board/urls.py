from django.urls import path
from . import views
from .views import MessageList, profile_view

urlpatterns = [
    path('', MessageList.as_view()),
    path('profile', profile_view, name='profile')
]
