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


def register_user(request):
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
        # return redirect('')

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, 'register_user.html', context)