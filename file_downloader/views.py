from django.shortcuts import render
from .forms import MyForm
from .models import MyModel
from .serializers import FileUploadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from PyPDF2 import PdfReader

from django.http import FileResponse


def upload_file(request):
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            html_file1_obj = form.cleaned_data['html_file1']
            html_file2_obj = form.cleaned_data['html_file2']
            my_model = MyModel(html_file1=html_file1_obj, html_file2=html_file2_obj)
            my_model.save()
            # Additional processing or redirect
    else:
        form = MyForm()
    return render(request, 'file_downloader/upload.html', {'form': form})



class FileUploadView(APIView):
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            html_file = serializer.validated_data['html_file']
            css_file = serializer.validated_data['css_file']
            # Perform additional processing with the uploaded files
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PreviewPDFView(APIView):
    def get(self, request, filename, format=None):
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'uploads/pdf', filename)
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
# The above API is used to view the pdf, http://localhost:8000/api/preview-pdf/<filename>/

class ExtractPDFView(APIView):
    def get(self, request, format=None):
        selected_files = request.GET.getlist('selected_files[]')  # Retrieve the selected file names
        pdf_folder = os.path.join(settings.MEDIA_ROOT, 'uploads/pdf')
        pdf_files = []

        # Loop through the PDF folder and extract information for selected files
        for filename in os.listdir(pdf_folder):
            if filename in selected_files:
                pdf_path = os.path.join(pdf_folder, filename)
                with open(pdf_path, 'rb') as f:
                    pdf = PdfReader(f)
                    num_pages = len(pdf.pages)
                    info = {
                        'filename': filename,
                        'num_pages': num_pages
                    }
                    pdf_files.append(info)

        return JsonResponse({'pdf_files': pdf_files})
#The above API is used to extract information about the PDF http://localhost:8000/api/extract-pdf/?selected_files[]=<filename>


class ExtractAllPDFView(APIView):
    def get(self, request, format=None):
        pdf_folder = os.path.join(settings.MEDIA_ROOT, 'uploads/pdf')
        pdf_files = []

        # Loop through the PDF folder and extract information
        for filename in os.listdir(pdf_folder):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(pdf_folder, filename)
                with open(pdf_path, 'rb') as f:
                    pdf = PdfReader(f)
                    num_pages = len(pdf.pages)
                    info = {
                        'filename': filename,
                        'num_pages': num_pages
                    }
                    pdf_files.append(info)

        return JsonResponse({'pdf_files': pdf_files})
#This API extracts information about all the PDF files present in the folder

