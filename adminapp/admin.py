from django.contrib import admin
from .models import *


@admin.register(FileModel)
class FileModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'download_count', 'email_count', 'created', 'updated']
    prepopulated_fields = {"slug": ['title']}
    list_filter = ['title', 'created']
    search_fields = [ 'title']
