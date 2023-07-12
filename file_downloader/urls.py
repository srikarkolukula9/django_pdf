from django.urls import path
from .views import upload_file, FileUploadView

app_name = 'file_downloader'

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
     path('api/upload/', FileUploadView.as_view(), name='file_upload'),
]