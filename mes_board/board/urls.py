from django.urls import path
from . import views
from .views import MessageList, MessageDetail, MessageCreate, MessageUpdate, MessageDelete, ResponseList, CommentDetail, \
    CommentEdit, CommentDelete, AddComment, AcceptResponseView, IndexView

CommentDetail

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('', MessageList.as_view(), name='message_list'),
    path('<int:pk>', MessageDetail.as_view(), name='message_detail'),
    path('create/', MessageCreate.as_view(), name='message_create'),
    path('<int:pk>/edit/', MessageUpdate.as_view(), name='message_edit'),
    path('<int:pk>/delete/', MessageDelete.as_view(), name='message_delete'),
    path('upload/', views.image_upload_view, name='image_upload'),
    path('responses/', ResponseList.as_view(), name='comments'),
    path('response/<int:pk>/', CommentDetail.as_view(), name='one_comment'),
    path('response/<int:pk>/edit/', CommentEdit.as_view(), name='comment_edit'),
    path('response/<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),
    path('response/create/', AddComment.as_view(), name='add_comment'),
    path('response/accept/<int:pk>/', AcceptResponseView.as_view(), name='accept_response'),




]
