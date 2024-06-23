from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model


class RegisterUserForm(UserCreationForm):
    email = forms.CharField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Enter email"}))
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Enter username"}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Enter password"}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Confirm password"}))
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)


    username = forms.CharField(label="Email", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter email"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}))

    def clean(self, *args, **kwags):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email_check = get_user_model().objects.filter(email=username)
        password_check = get_user_model().objects.filter(password=password)

        if password_check == None:
            raise forms.ValidationError("Incorrect password")
        
        if email_check == None:
            raise forms.ValidationError('Incorrect Email address')
        return super(LoginUserForm, self).clean(*args, **kwags)

class ChangePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Enter new password"}))
    new_password2 = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder":"Confirm new password"}))

    class Meta:
        model = get_user_model()
        feilds = ['new_password1', 'new_password2']

    def clean(self, *args, **kwags):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if len(new_password1) < 5 and len(new_password2) < 5:
            raise forms.ValidationError("Your passsword should have more than 5 characters")
        return super(ChangePasswordForm, self).clean(*args, **kwags)

class ResetPasswordForm(PasswordResetForm):
    email =forms.CharField(label="Email",widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email"}))

    def clean(self, *args, **kwags):
        return super(ResetPasswordForm, self).clean(*args, **kwags)
