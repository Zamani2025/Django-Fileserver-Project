from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.indexPage, name="home"),
    path('register/', view=views.registerPage, name="register"),
    path('search-file/', view=views.searchFilePage, name="search"),
    path('login/', view=views.loginPage, name="login"),
    path('logout/', view=views.logoutPage, name="logout"),
    path('password_change/', view=views.changePasswordPage, name="change-password"),
    path('password-reset/', view=views.passwordReset, name="password-reset"),
    path('password-reset-confirm/<uidb64>/<token>/', view=views.passwordResetConfirm, name="password-reset-confirm"),
    path('verify-email-confirm/<uidb64>/<token>/', view=views.verifyEmailConfirm, name="verify-email-confirm"),
    path('download/<int:file_id>/', views.downloadFile, name='download_file'),
    path('send-file-to-email/<int:file_id>/', views.sendFileToEmail, name='send_file'),
]