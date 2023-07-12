from django.db import models
from django.core.exceptions import ValidationError

def validate_html_file_extension(value):
    valid_extensions = ['.html']
    file_extension = value.name.lower().split('.')[-1]
    if file_extension not in valid_extensions:
        raise ValidationError("Only HTML files are allowed.")

def validate_css_file_extension(value):
    valid_extensions = ['.css']
    file_extension = value.name.lower().split('.')[-1]
    if file_extension not in valid_extensions:
        raise ValidationError("Only CSS files are allowed.")

class MyModel(models.Model):
    id= models.AutoField(primary_key=True)
    html_file = models.FileField(upload_to='uploads/', validators=[validate_html_file_extension])
    css_file = models.FileField(upload_to='uploads/', validators=[validate_css_file_extension])
