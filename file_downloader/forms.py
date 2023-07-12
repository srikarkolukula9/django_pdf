from django import forms

from file_downloader.models import validate_html_file_extension, validate_css_file_extension

class MyForm(forms.Form):
    html_file = forms.FileField(label='HTML File', validators=[validate_html_file_extension])
    css_file = forms.FileField(label='CSS File', validators=[validate_css_file_extension])
