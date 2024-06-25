from django import forms
from . models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

# Change Password Form
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

# File Form
class FileForm(forms.ModelForm):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter file title"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter description"}))
    file = forms.FileField(widget=forms.FileInput(attrs={"class":"form-control", "rows":5}))
    class Meta:
        model = FileModel
        fields = ['title', 'description', 'file']

    def clean(self, *args, **kwags):
        title = self.cleaned_data.get('title')
        title_check = FileModel.objects.filter(title=title)
        if title_check.exists():
            raise forms.ValidationError("This title slug already exists")
        return super(FileForm, self).clean(*args, **kwags)
