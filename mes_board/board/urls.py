from django.urls import path
from . import views
from .views import MessageList, MessageDetail, MessageCreate

urlpatterns = [
    path('', MessageList.as_view()),
    path('<int:pk>', MessageDetail.as_view()),
    path('create/', MessageCreate.as_view(), name='message_create'),
    path('edit/<int:pk>', MessageDetail.as_view(), name='message_edit'),
    path('delete/<int:pk>', MessageDetail.as_view(), name='message_delete'),



]
