from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.dashboardPage, name="admin-dashboard"),
    path('admin-search', view=views.searchFilePage, name="admin-search"),
    path('admin-change-password/', view=views.adminchangePasswordPage, name="admin-change-password"),
    path('all-files/', view=views.filePage, name="all-files"),
    path('add-file/', view=views.addFilePage, name="add-file"),
    path('edit-file/<int:pk>/', view=views.editFilePage, name="edit-file"),
    path('delete-file/<int:pk>/', view=views.deleteFile, name="delete-file"),
]