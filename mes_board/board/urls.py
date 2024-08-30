from django.urls import path
from . import views
from .views import MessageList, MessageDetail

urlpatterns = [
    path('', MessageList.as_view()),
    path('<int:pk>', MessageDetail.as_view()),
]
