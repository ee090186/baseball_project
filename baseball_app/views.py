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