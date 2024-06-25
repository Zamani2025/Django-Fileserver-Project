from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . forms import *
from . models import *
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth import logout
from django.db.models.query_utils import Q

# Admin Change Password Page
@login_required(login_url='login')
def adminchangePasswordPage(request):
    if request.user.is_staff == False:
        return redirect('home')
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="Your password has been changed")
            logout(request=request)
            return redirect('login')
    else:
        form = ChangePasswordForm(user=request.user)
    title = "Lizzy File Server Admin Change Password"
    context = {'title': title, "form": form}
    return render(request=request, template_name="admin/admin_change_password.html", context=context)

# Admin Dashboard Page
@login_required(login_url='login')
def dashboardPage(request):
    if request.user.is_staff == False:
        return redirect('home')
    title = "Lizzy File Server Admin Dashboard"
    files = FileModel.objects.all()
    context = {"title": title, "files": files}
    return render(request=request, template_name="admin/dashboard.html", context=context)

# Admin All Files Page
@login_required(login_url='login')
def filePage(request):
    if request.user.is_staff == False:
        return redirect('home')    
    title = "Lizzy File Server All Files"
    form = FileForm()
    files = FileModel.objects.all()
    context = {"title": title, "form": form, "files": files}
    return render(request=request, template_name='admin/files.html', context=context)

# Admin Add File Method
@login_required(login_url='login')
def addFilePage(request):
    if request.user.is_staff == False:
        return redirect('home')
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.upload_by = request.user
            file.save()
            messages.success(request=request, message=file.title + " created successfully")
            return redirect('all-files')
        else:
            messages.warning(request=request, message=form.errors)
            return redirect('all-files')

# Admin Edit File Method
@login_required(login_url='login')
def editFilePage(request, pk):
    if request.method == 'POST':
        title = request.POST.get('title')
        edit_file = request.FILES.get('file')
        description = request.POST.get('description')
        file = FileModel.objects.get(id=pk)
        file.title = title
        file.description = description
        if request.FILES.get('file'):
            file.file = edit_file
        file.slug = slugify(title)
        file.save()
        messages.success(request=request, message=f"File updated successfully")
        return redirect('all-files')

# Admin Delete File Method
@login_required(login_url='login')
def deleteFile(request, pk):
    if request.user.is_staff == False:
        return redirect('home')
    file = FileModel.objects.get(id=pk)
    file.delete()
    messages.success(request=request, message= file.title + " deleted successfully!")
    return redirect('all-files')

# Admin Search File Method
def searchFilePage(request):
    q = request.POST.get('q')
    title = "Searc File"
    if request.method == "POST":
        files = FileModel.objects.filter(Q(title__contains=q) | Q(description__contains=q))
    context = {"files": files, "title": title}
    return render(request=request, template_name="admin/search_page.html", context=context)
