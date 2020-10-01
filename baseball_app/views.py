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
from .models import Profile, Situation, Pitting, Batting, ContactedResults, UncontactedResults


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

        if 'discrimination' not in request.POST:
            # 打席結果のPOST送信時の処理
            if 'contacted_results' in request.POST:
                contacted_results_form = ContactedResultsForm(request.POST)
                batting = Batting.objects.get(id=request.POST['batting_id'])
                if contacted_results_form.is_valid():
                    contacted_result = contacted_results_form.save(commit=False)
                    contacted_result.batting = batting
                    contacted_result.save()
                    return redirect('data')
                else:
                    context.update({
                        'contacted_results_form': contacted_results_form,
                        'batting': batting,
                    })
                    render(request, 'data.html', context)

            elif 'uncontacted_results' in request.POST:
                uncontacted_results_form = UncontactedResultsForm(request.POST)
                batting = Batting.objects.get(id=request.POST['batting_id'])
                if uncontacted_results_form.is_valid():
                    uncontacted_result = uncontacted_results_form.save(commit=False)
                    uncontacted_result.batting = batting
                    uncontacted_result.save()
                    return redirect('data')
                else:
                    context.update({
                        'uncontacted_results_form': uncontacted_results_form,
                        'batting': batting
                    })
                    render(request, 'data.html', context)

            # 最初のピッチャーとバッター名入力後のフォーム準備
            else:
                situation_form = SituationForm() # これからフォームを入力していくので引数なし
                pitting_form = PittingForm()
                batting_form = BattingForm()
                context.update(
                    {'situation_form': situation_form,
                    'pitting_form': pitting_form,
                    'batting_form': batting_form,}
                )

        # シチュエーション以下各フォームへの入力データありの場合(2回目以降)の共通処理
        else:
            situation_form = SituationForm(request.POST) # 前回入力データを引き継いでフォームに表示させる
            pitting_form = PittingForm(request.POST)
            batting_form = BattingForm(request.POST)
            if situation_form.is_valid() and pitting_form.is_valid() and batting_form.is_valid():
                situation = situation_form.save() # 入力データを保存
                situation.save()
                pitting = pitting_form.save(commit=False)
                pitting.situation = situation
                pitting.user = pitcher
                pitting.save()
                batting = batting_form.save(commit=False)
                batting.pitting = pitting
                batting.user = batter
                batting.save()

                # 打席結果未定時のフォーム準備
                if request.POST['discrimination'] == 'undecided':
                    context.update({
                        'situation_form': situation_form,
                        'pitting_form': pitting_form,
                        'batting_form': batting_form,
                        })

                # 以下二つの条件分岐は、打席結果確定時のフォーム準備・データ保存
                elif request.POST['discrimination'] == 'decided_with_contacted':
                    contacted_results_form = ContactedResultsForm()
                    context.update({
                        'contacted_results_form': contacted_results_form,
                        'batting': batting, # 打席結果保存する際に、該当するbattingと紐づけるため一緒に送る
                        })

                elif request.POST['discrimination'] == 'decided_with_uncontacted':
                    uncontacted_results_form = UncontactedResultsForm()
                    context.update({
                        'uncontacted_results_form': uncontacted_results_form,
                        'batting': batting, 
                        })

            # 入力が有効でなかった場合
            else:
                context.update({
                    'situation_form': situation_form,
                    'pitting_form': pitting_form,
                    'batting_form': batting_form,
                    })

        return render(request, 'data.html', context)
            
    return render(request, 'data.html')


