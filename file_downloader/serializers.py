from rest_framework import serializers
from .models import MyModel

class FileUploadSerializer(serializers.Serializer):
    html_file = serializers.FileField(allow_empty_file=False, allow_null=False)
    css_file = serializers.FileField(allow_empty_file=False, allow_null=False)

    def create(self, validated_data):
        html_file = validated_data.pop('html_file')
        css_file = validated_data.pop('css_file')
        instance = MyModel(**validated_data)
        instance.html_file.save(html_file.name, html_file)
        instance.css_file.save(css_file.name, css_file)
        instance.save()
        return instance



class FileUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()
