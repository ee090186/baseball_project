from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import request
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import ProfileForm, UserCreateForm



def registerview(request):
    # or NoneでGet時はNoneとなり、引数なしのフォームを作る。
    user_form = UserCreateForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():

        # Userモデルの処理。ログインできるようis_activeをTrueにし保存。
        user = user_form.save(commit=False)
        user.is_active = True
        user.save()

        # Profileモデルの処理。Userモデルと紐づけ。
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        return redirect('home')

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, 'login_register/register.html', context)


def loginview(request):
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        user = authenticate(request, username=username_data, password=password_data)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'login_register/login.html')


def logoutview(request):
    logout(request)
    return redirect('login')


def homeview(request):
    params = {
        'login_user': request.user,
    }

    return render(request, 'home.html', params)
    