from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from . serializers import FileModelSerializer
from adminapp.models import FileModel
from rest_framework.decorators import APIView
from django.shortcuts import get_object_or_404


class FileList(APIView):
    def get(self, request:Request):
        files = FileModel.objects.all()
        serializer = FileModelSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request:Request):
        serilizer = FileModelSerializer(data=request.data)
        if serilizer.is_valid(raise_exception=True):
            serilizer.save()
            return Response(serilizer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDetail(APIView):
    def get_obj(self, pk):
        return get_object_or_404(FileModel, pk=pk)
    
    def get(self, request:Request, pk):
        file = self.get_obj(pk=pk)
        serializer = FileModelSerializer(file)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request:Request, pk):
        file = self.get_obj(pk=pk)
        serializer = FileModelSerializer(instance=file, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request:Request, pk):
        file = self.get_obj(pk=pk)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
