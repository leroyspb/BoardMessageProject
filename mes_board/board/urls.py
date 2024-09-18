from django.urls import path
from . import views
from .views import MessageList, MessageDetail, MessageCreate, MessageUpdate, MessageDelete, ResponseList, \
    CommentEdit, CommentDelete, AcceptResponseView, IndexView, response_status_update, ResponseCreate


urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('', MessageList.as_view(), name='message_list'),
    path('<int:pk>', MessageDetail.as_view(), name='message_detail'),
    path('create/', MessageCreate.as_view(), name='message_create'),
    path('<int:pk>/edit/', MessageUpdate.as_view(), name='message_edit'),
    path('<int:pk>/delete/', MessageDelete.as_view(), name='message_delete'),
    path('upload/', views.message_media, name='files_upload'),
    path('responses/', ResponseList.as_view(), name='response'),
    path('response/<int:pk>/status', response_status_update, name='response_status'),
    path('response/create/', ResponseCreate.as_view(), name='response_create'),
    path('response/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
    path('response/<int:pk>/edit/', CommentEdit.as_view(), name='comment_edit'),


    path('response/accept/<int:pk>/', AcceptResponseView.as_view(), name='accept_response'),




]
