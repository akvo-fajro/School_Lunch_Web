from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Announcement
from .forms import LoginForm,ChangePasswordForm

# Create your views here.

# home page
# url : /
def homepage_view(request,*args,**kargs):
    announce_list = [a.announce for a in Announcement.objects.all()]
    announce_list.reverse()
    context = {
        'announce_list':announce_list
    }
    return render(request,'users_pages/home.html',context)


# profile page (displa the user file and the change password button)
# url : /accounts/profile
@login_required(login_url='login')
def profile_view(request,*args,**kargs):
    return render(request,'users_pages/profile.html',{})


# login page
# url : /accounts/login
def login_view(request,*args,**kargs):
    form = LoginForm()
    err = False
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            if 'next' in request.GET.keys():
                return redirect(request.GET.get('next'))
            return redirect('/accounts/profile')
        else:
            err = True
    context = {
        'form':form,
        'error':err,
    }
    return render(request,'users_pages/login.html',context)


# change password pages
# url : /accounts/change_password
@login_required(login_url='login')
def change_password_view(request,*args,**kargs):
    form = ChangePasswordForm()
    err = False
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            err = True
        else:
            user = User.objects.get(username=request.user)
            user.set_password(password1)
            user.save()
            logout(request)
            return redirect('/accounts/login')
    context = {
        'form':form,
        'error':err,
    }
    return render(request,'users_pages/change_password.html',context)


# logout function (this function does not display)
# url : /accounts/logout
def logout_function(request,*args,**kargs):
    logout(request)
    return redirect('/accounts/login')