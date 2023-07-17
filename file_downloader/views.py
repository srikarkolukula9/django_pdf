from django.shortcuts import render
from .forms import MyForm
from .models import MyModel
from .serializers import FileUploadSerializer, FileUploadCSVSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
from PyPDF2 import PdfReader

from django.http import FileResponse
from django.core.files.storage import default_storage

from django.views.generic import TemplateView

from django.http import HttpResponseNotFound
from django.http import HttpResponse

import csv

from django.template.loader import get_template
import pdfkit




def generate_pdf(request):
    html_path = os.path.join('uploads', 'index.html')
    css_path = os.path.join('uploads', 'style.css')
    pdf_output_path = os.path.join('uploads', 'pdf', 'output.pdf')

    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': 'UTF-8',
        'no-outline': None
    }

    pdfkit.from_file(html_path, pdf_output_path, options=options, css=css_path)

    with open(pdf_output_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'

    return response







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
            # html_path = default_storage.save('index.html', html_file)

            css_file = serializer.validated_data['css_file']
            # css_path = default_storage.save('static.css' , css_file)
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



class PreviewHTMLAPIView(APIView):
    def get(self, request, filename, format=None):
        uploads_folder = 'uploads'  # Path to the uploads folder

        html_filepath = os.path.join(uploads_folder, filename)
        css_filepath = os.path.join(uploads_folder, 'style.css')

        if os.path.isfile(html_filepath) and os.path.isfile(css_filepath):
            with open(html_filepath, 'r') as html_file, open(css_filepath, 'r') as css_file:
                html_content = html_file.read()
                css_content = css_file.read()

            combined_html = f'<style>{css_content}</style>\n{html_content}'

            return Response({'combined_html': combined_html})

        return HttpResponseNotFound('File not found')








import os
from django.http import HttpResponseNotFound, HttpResponse

def preview_html(request, filename):
    uploads_folder = 'uploads'  # Path to the uploads folder

    html_filepath = os.path.join(uploads_folder, filename)
    css_filepath = os.path.join(uploads_folder, 'style.css')

    if os.path.isfile(html_filepath) and os.path.isfile(css_filepath):
        with open(html_filepath, 'r') as html_file, open(css_filepath, 'r') as css_file:
            html_content = html_file.read()
            css_content = css_file.read()

        combined_html = f'<style>{css_content}</style>\n{html_content}'

        return HttpResponse(combined_html, content_type='text/html')

    return HttpResponseNotFound('File not found')





def delete_uploads(request):
    upload_folder = os.path.join(settings.MEDIA_ROOT, 'uploads')

    try:
        # Iterate through files within the uploads folder and delete them
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        return JsonResponse({'message': 'All files deleted successfully.'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





class CSVFileUploadView(APIView):
    def post(self, request, format=None):
        serializer = FileUploadCSVSerializer(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.validated_data['csv_file']
            
            # Get the upload folder path
            upload_folder = os.path.join(settings.MEDIA_ROOT, 'uploads')
            
            # Create the uploads folder if it doesn't exist
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            # Save the uploaded CSV file to the uploads folder
            csv_path = os.path.join(upload_folder, csv_file.name)
            with open(csv_path, 'wb') as file:
                file.write(csv_file.read())

            # Perform additional processing with the uploaded file if needed

            return Response(status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class CSVColumnNamesAPIView(APIView):
    def get(self, request, format=None):
        csv_file_name = 'data.csv'
        upload_folder = os.path.join(settings.MEDIA_ROOT, 'uploads')
        csv_file_path = os.path.join(upload_folder, csv_file_name)

        if not os.path.exists(csv_file_path):
            return Response({'error': 'CSV file not found.'}, status=400)

        column_names = []

        try:
            with open(csv_file_path, 'r') as file:
                reader = csv.reader(file)
                if reader:
                    column_names = next(reader)

        except Exception as e:
            return Response({'error': str(e)}, status=500)

        return Response({'column_names': column_names})
    
    
import os
from django.http import HttpResponse, HttpResponseNotFound

def edit_html(request, filename):
    uploads_folder = 'uploads'  # Path to the uploads folder

    html_filepath = os.path.join(uploads_folder, filename)
    css_filepath = os.path.join(uploads_folder, 'style.css')

    if request.method == 'POST':
        # Handle form submission for editing the HTML file
        new_html_content = request.POST.get('html_content', '')
        with open(html_filepath, 'w') as html_file:
            html_file.write(new_html_content)

    if os.path.isfile(html_filepath) and os.path.isfile(css_filepath):
        with open(html_filepath, 'r') as html_file, open(css_filepath, 'r') as css_file:
            html_content = html_file.read()
            css_content = css_file.read()

        # Generate the HTML page with the CSS and HTML content
        combined_html = f'''
            <style>
                .container {{
                    display: flex;
                }}
                .preview {{
                    flex: 1;
                    padding-right: 10px;
                }}
                .editor {{
                    flex: 1;
                }}
                textarea {{
                    width: 100%;
                    height: 100vh;
                }}
            </style>
            <div class="container">
                <div class="preview">
                    <h2>Preview:</h2>
                    <div>{html_content}</div>
                </div>
                <div class="editor">
                    <h2>Edit:</h2>
                    <form method="post">
                        <textarea name="html_content" rows="10" cols="50">{html_content}</textarea>
                        <br>
                        <input type="submit" value="Save">
                    </form>
                </div>
            </div>
        '''

        return HttpResponse(combined_html, content_type='text/html')

    return HttpResponseNotFound('File not found')



# class CSVHeaderAPIView(APIView):
#     def post(self, request, format=None):
#         serializer = FileUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             csv_file = serializer.validated_data['csv_file']
            
#             # Get the upload folder path
#             upload_folder = os.path.join(settings.MEDIA_ROOT, 'uploads')
            
#             # Create the uploads folder if it doesn't exist
#             if not os.path.exists(upload_folder):
#                 os.makedirs(upload_folder)

#             # Save the uploaded CSV file to the uploads folder
#             csv_path = os.path.join(upload_folder, csv_file.name)
#             with open(csv_path, 'wb') as file:
#                 file.write(csv_file.read())

#             # Perform additional processing with the uploaded file if needed
#             headers = []
#             try:
#                 with open(csv_path, 'r') as file:
#                     reader = csv.reader(file)
#                     headers = next(reader)
#             except Exception as e:
#                 return Response({'error': str(e)}, status=500)

#             return Response({'headers': headers}, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# def delete_uploads_uploads(request):
#     upload_folder = os.path.join(settings.MEDIA_ROOT, 'uploads/uploads')

#     try:
#         # Iterate through files within the uploads folder and delete them
#         for filename in os.listdir(upload_folder):
#             file_path = os.path.join(upload_folder, filename)
#             if os.path.isfile(file_path):
#                 os.remove(file_path)

#         return JsonResponse({'message': 'All files deleted successfully.'})

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)







# class RenderHTMLView(TemplateView):
#     def get_template_names(self):
#         filename = self.kwargs['filename']
#         html_file_path = os.path.join(settings.MEDIA_ROOT, 'uploads/html', filename)
#         css_file_path = os.path.join(settings.MEDIA_ROOT, 'uploads/css', filename)

#         # Generate a unique template name for each request
#         unique_template_name = f'rendered_{filename}.html'

#         # Create a new HTML file by combining the uploaded HTML and CSS
#         with open(html_file_path, 'r') as html_file:
#             html_content = html_file.read()

#         with open(css_file_path, 'r') as css_file:
#             css_content = css_file.read()

#         rendered_html = f'<style>{css_content}</style>\n{html_content}'

#         # Save the combined HTML and CSS content to a new template file
#         template_dir = os.path.join(settings.BASE_DIR, 'rendered_templates')
#         os.makedirs(template_dir, exist_ok=True)  # Create the 'rendered_templates' directory if it doesn't exist

#         template_path = os.path.join(template_dir, unique_template_name)
#         with open(template_path, 'w') as template_file:
#             template_file.write(rendered_html)

#         return [os.path.join('rendered_templates', unique_template_name)]


