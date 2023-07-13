from django.urls import path
from .views import upload_file, FileUploadView, ExtractPDFView, PreviewPDFView, ExtractAllPDFView

app_name = 'file_downloader'

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('api/upload/', FileUploadView.as_view(), name='file_upload'),
    path('api/extract-pdf/', ExtractPDFView.as_view(), name='extract_pdf'),
    path('api/preview-pdf/<str:filename>/', PreviewPDFView.as_view(), name='preview_pdf'),
    path('api/extract-all-pdf/', ExtractAllPDFView.as_view(), name='extract_all_pdf'),
]