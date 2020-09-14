from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import request
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.
def signupview(request):
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        try:
            user = User.objects.create_user(username_data, '', password_data)
        except IntegrityError:
            return render(request, 'signup.html', {'error':' このユーザーは既に登録されています。 '})
    else:
        return render(request, 'signup.html', {})

    return render(request, 'signup.html', {})


from django.shortcuts import render, redirect
from .forms import ProfileForm, UserCreateForm


def register_user(request):
    user_form = UserCreateForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():

        # Userモデルの処理。ログインできるようis_activeをTrueにし保存
        user = user_form.save(commit=False)
        user.is_active = True
        user.save()

        # Profileモデルの処理。↑のUserモデルと紐づけましょう。
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        return redirect("testapp:index")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, 'register_user.html', context)