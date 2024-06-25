from django.urls import path
from . import views

urlpatterns = [
    path('files/', view=views.FileList.as_view()),
    path('files/<pk>', view=views.FileDetail.as_view()),
]
