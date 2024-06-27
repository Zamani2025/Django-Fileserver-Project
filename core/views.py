from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from . forms import ChangePasswordForm, ResetPasswordForm
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from . token import account_activation_token
from django.contrib.auth import get_user_model
from adminapp.models import *
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponse
from django.conf import settings
import os

# Email Verification Method
def verifyEmailConfirm(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user=user, token=token):
        user.is_active = True
        user.save()
        messages.success(request=request, message="Thank you for your email confirmation. Now you can login your account!")
        return redirect('login')
    
    else:
        messages.warning(request=request, message="Activation link is invalid")
    
    return redirect('login')

# Home Page Method
@login_required(login_url="login")
def indexPage(request):
    files = FileModel.objects.all()
    p = Paginator(files, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number) 
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    title = "Lizzy File Server - Home"
    context = {"title": title, "page_obj": page_obj}
    return render(request=request, template_name='home/index.html', context=context) 

# Search File Page Method
def searchFilePage(request):
    q = request.POST.get('q')
    title = "Lizzy File Server - Search File"
    if request.method == "POST":
        files = FileModel.objects.filter(Q(title__contains=q) | Q(description__contains=q))
        p = Paginator(files, 6)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number) 
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
    context = {"page_obj": page_obj, "title": title}
    return render(request=request, template_name="home/search_page.html", context=context)

# Login Page Method
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        if not get_user_model().objects.filter(email=email).exists():
            messages.warning(request=request, message="Invalid email provided")
            return redirect('login')
    
        user = authenticate(request=request, email=email, password=password)
        if user is not None:
            login(request=request, user=user)
            return redirect('home')
        else:
            messages.warning(request=request, message="Incorrect Password")
            return redirect('login')
    title = "Lizzy File Server - Login"
    context = {"title": title}
    return render(request=request, template_name='home/login.html', context=context)

# Registration Page Method
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.warning(request=request, message="Password does not match")
            return redirect('register')
        
        if len(password) <= 7:
            messages.warning(request=request, message="Password must be >= 8")
            return redirect('register')
            
        if get_user_model().objects.filter(email=email).exists():
            messages.warning(request=request, message="User with this email already exists")
            return redirect('register')
        
        if get_user_model().objects.filter(username=username).exists():
            messages.warning(request=request, message="User with this username already exists")
            return redirect('register')

        user = get_user_model().objects.create(
            username= username,
            email=email,
            password=password
        )
        user.set_password(password)
        user.is_active = False
        user.save()
        current_site = get_current_site(request=request)
        subject = "Activate Your Account"
        message = render_to_string(
            template_name='home/verify_email_message.html',
            request=request,
            context= {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user=user),
                'protocol': "https" if request.is_secure() else "http"
            }
        )
        to_email = request.POST.get('email')
        email = EmailMessage(subject, message, to=[to_email])
        email.content_subtype = 'html'
        if email.send():
            messages.success(request=request, message="Please confirm your email address to complete the registration")
            return redirect('login')
        else:
            messages.success(request=request, message=f'Problem sending email to {to_email}, check if you typed it correctly!')
            return redirect('login')
        return redirect('login')
    title = "Lizzy File Server - Register"
    context = {"title": title}
    return render(request=request, template_name='home/register.html', context=context)

# Logout Page Method
def logoutPage(request):
    logout(request=request)
    messages.success(request=request, message="Thanks for spending some quality time with the web site today.")
    return redirect('login')

# Change Password Page Method
@login_required(login_url='login')
def changePasswordPage(request):
    
    title = "Lizzy File Server - Change Password"
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="Your password has been changed")
            logout(request=request)
            return redirect('login')
    else:
        form = ChangePasswordForm(user=request.user)
    context = {'title': title, "form": form}
    return render(request=request, template_name="home/change_password.html", context=context)

# Password Reset Page Method
def passwordReset(request):
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get("email")
            associated_user = get_user_model().objects.filter(email=user_email).first()
            if associated_user:
                subject = "Password Reset Request"
                message = render_to_string(
                    template_name='home/reset_password_message.html',
                    request=request,
                    context= {
                        "user": associated_user,
                        "domain": get_current_site(request=request).domain,
                        "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                        "token": account_activation_token.make_token(user=associated_user),
                        'protocol': "https" if request.is_secure() else "http"
                    }
                )
                email = EmailMessage(subject, message, to=[associated_user.email])
                email.content_subtype = 'html'
                if email.send():
                    messages.success(
                        request=request, 
                        message="""
                                Password reset sent.
                                we've emailed you instructions for setting your password, 
                                if an account exists with the email you entered.
                            """
                        )
                else:
                    messages.success(request=request, message=f'Problem sending reset password email, SERVER PROBLEM')
                    return redirect('login')
            else:
                messages.warning(request=request,message="Please enter a valid email")
    else:
        form = ResetPasswordForm()
    title = "Lizzy File Server - Password Reset"
    context = {"form": form, "title": title}
    return render(request=request, template_name="home/password_reset.html", context=context)

# Password Reset Confirmation Method
def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user=user, token=token):
        if request.method == "POST":
            form = ChangePasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request=request, message="Your password has been set. You can go ahead and login now")
                return redirect('login')
        else:
            form = ChangePasswordForm(user=user)
    
    else:
        messages.warning(request=request, message="Activation link is invalid")
    context = {"form": form}
    return render(request=request, template_name="home/reset_password_confirm.html", context=context)

# Download File Method
@login_required(login_url="login")
def downloadFile(request, file_id):
    file_obj = FileModel.objects.get(pk=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(file_obj.file))
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.file.name}"'
        file_obj.download()
        return response

# Send File To Email Method  
@login_required(login_url="login")    
def sendFileToEmail(request, file_id):
    if request.method == "POST":

        file_obj = FileModel.objects.get(pk=file_id)

        recipient_email = request.POST.get('email')

        subject = file_obj.title
        message = file_obj.description
        email = EmailMessage(subject, message, to=[recipient_email])
        email.attach_file(file_obj.file.path)

        if email.send(fail_silently=False):
            file_obj.sendEmail()
            messages.success(request=request, message=f"File has been send to {recipient_email} now!")
            return redirect('home')
        else:
            messages.warning(request=request, message="Incorrect email address provided")
            return redirect('home')
        