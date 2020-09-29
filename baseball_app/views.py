from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import request
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileForm, UserCreateForm, SituationForm, PittingForm, BattingForm, ContactedResultsForm, UncontactedResultsForm
from .models import Profile


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


@login_required()
def homeview(request):
    params = {
        'login_user': request.user,
    }

    return render(request, 'home.html', params)
    
@login_required()
def updateview(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = Profile.objects.get(user_id=pk)
    user_form = UserCreateForm(request.POST or None, instance=user)
    profile_form = ProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        login(request, user) # if文部分でセッションが切れている（原因不明）ので、login_requiredにかからないよう追記
        return redirect("home")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        'login_user': request.user
    }
    return render(request, 'update.html', context)


@login_required()
def listview(request):
    """1.ログイン中のユーザーを取り出す。
       2.そのユーザーのプロフィールインスタンスを取り出す。
       3.そのプロフィールインスタンスからチーム名を取り出す。
       4.そのチーム名を持つプロフィールインスタンスのクエリセットをteammate_profileへ代入"""

    login_user = request.user
    my_team = Profile.objects.get(user=login_user).team
    teammate_profile = Profile.objects.filter(team=my_team)
    teammate_user = User.objects.filter(profile__team__in=teammate_profile)
    context = {
        'teammate_profile': teammate_profile,
        'teammate_user': teammate_user,
        'login_user': login_user,
    }
    return render(request, 'list.html', context)


@login_required()
def deleteview(request):
    user = request.user
    
    if request.method == 'POST':
        user.delete()
        return redirect('login')
    
    return render(request, 'delete.html')



@login_required()
def dataview(request):
    if request.method == 'POST':
        # POST送信時の共通処理・準備
        pitcher = User.objects.get(username=request.POST['pitchername']) # 以下ピッチャーとバッターのプロフィール側の名前取り出し部分長いためいずれ改善
        batter = User.objects.get(username=request.POST['battername'])
        pitchername = Profile.objects.get(user=pitcher).name
        battername = Profile.objects.get(user=batter).name
        context = {
            'pitchername': pitchername,
            'battername': battername,
            'pitcher': pitcher,
            'batter': batter,
            'login_user': request.user,
        }

        # 最初のピッチャーとバッター名入力後および、打席結果未定のPOST送信時のフォーム準備
        if 'discrimination' not in request.POST or request.POST['discrimination'] == 'undecided':
            situation_form = SituationForm(request.POST or None)
            pitting_form = PittingForm(request.POST or None)
            batting_form = BattingForm(request.POST or None)
            context.update(
                {'situation_form': situation_form,
                'pitting_form': pitting_form,
                'batting_form': batting_form,}
            )
        # 以下二つの条件分岐は、打席結果確定時のフォーム準備
        elif request.POST['discrimination'] == 'decided_with_contacted':
            contacted_results_form = ContactedResultsForm(request.POST or None)
            context.update({'contacted_results_form': contacted_results_form,})

        elif request.POST['discrimination'] == 'decided_with_uncontacted':
            uncontacted_results_form = UncontactedResultsForm(request.POST or None)
            context.update({'uncontacted_results_form': uncontacted_results_form,})

        return render(request, 'data.html', context)
        
    return render(request, 'data.html')


