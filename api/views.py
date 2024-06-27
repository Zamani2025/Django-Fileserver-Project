from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from . serializers import FileModelSerializer
from adminapp.models import FileModel
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class FileList(APIView):
    def get(self, request:Request):
        files = FileModel.objects.all()
        serializer = FileModelSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FileDetail(APIView):
    def get_obj(self, pk):
        return get_object_or_404(FileModel, pk=pk)
    
    def get(self, request:Request, pk):
        file = self.get_obj(pk=pk)
        serializer = FileModelSerializer(file)
        return Response(serializer.data, status=status.HTTP_200_OK)
       
    def delete(self, request:Request, pk):
        file = self.get_obj(pk=pk)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
