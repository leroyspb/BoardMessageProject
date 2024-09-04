from django.urls import path
from . import views
from .views import MessageList, MessageDetail, MessageCreate, MessageUpdate, MessageDelete

urlpatterns = [
    path('', MessageList.as_view(), name='message_list'),
    path('<int:pk>', MessageDetail.as_view(), name='message_detail'),
    path('create/', MessageCreate.as_view(), name='message_create'),
    path('<int:pk>/edit/', MessageUpdate.as_view(), name='message_edit'),
    path('<int:pk>/delete/', MessageDelete.as_view(), name='message_delete'),



]
