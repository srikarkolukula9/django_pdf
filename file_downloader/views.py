from django.shortcuts import render
from .forms import MyForm
from .models import MyModel
from .serializers import FileUploadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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

