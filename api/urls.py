from django.urls import path
from .views import *

urlpatterns = [
    path('upload', UploadFileView.as_view(), name='upload-file'),
    path('execute-query', ExecuteQueryView.as_view(), name='execute-query'),
    path('get-chat-history', GetChatHistoryView.as_view(), name='get-chat-history'),
    path('get-resumes', GetResumesView.as_view(), name='get-resumes'),
]