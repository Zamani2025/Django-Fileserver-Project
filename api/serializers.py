from rest_framework import serializers
from adminapp.models import FileModel


class FileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = ['id', 'title', 'description', 'file', 'created']