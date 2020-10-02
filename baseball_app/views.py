from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Avg, Max, Min, Sum
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

    if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            # Userモデルの処理。ログインできるようis_activeをTrueにし保存。(意図した動作しないため、最後にlogin()部分追加)
            user = user_form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)
            # Profileモデルの処理。Userモデルと紐づけ。
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, '"' + user.username + '"' + 'の登録が完了しました。')
            return redirect('home')
        else:
            messages.error(request, '不正な入力があります。修正してください。')

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
            messages.success(request, 'ログインしました。')
            return redirect('home')
        else:
            messages.error(request, 'ログインに失敗しました。ユーザー名とパスワードが間違いないか確認してください。')
            return redirect('login')

    return render(request, 'login_register/login.html')


def logoutview(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('login')


@login_required()
def homeview(request):
    return render(request, 'home.html')
    
@login_required()
def updateview(request, pk):
    # modelクラスのインスタンス作成(既存のレコードより)
    user = get_object_or_404(User, pk=pk)
    profile = Profile.objects.get(user_id=pk)
    # modelformクラスのインスタンス作成(更新したいデータはrequest.POSTで、既存レコードのデータはinstanceで指定)
    user_form = UserCreateForm(request.POST or None, instance=user)
    profile_form = ProfileForm(request.POST or None, instance=profile)

    if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # if文部分でセッションが切れている?（原因不明）ので、login_requiredにかからないよう追記
            login(request, user)
            messages.success(request, '登録情報を変更しました。')
            return redirect("home")

        # フォームへの入力がvalidでない場合
        else:
            messages.error(request, '不正なデータを入力しています。修正してください。')

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    # 初回GET時、もしくはif ~ .is_valid()でvalidでなかった場合
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
    }
    return render(request, 'list.html', context)


@login_required()
def deleteview(request):
    user = request.user
    
    if request.method == 'POST':
        messages.success(request, '"' + user.username + '"' + 'の登録を削除しました。')
        user.delete()
        return redirect('login')
    
    return render(request, 'delete.html')


@login_required()
def dataview(request):
    if request.method == 'POST':
        # POST送信時の共通処理・準備
        try:
            pitcher = User.objects.get(username=request.POST['pitchername']) # 以下ピッチャーとバッターのプロフィール側の名前取り出し部分いずれ改善
            batter = User.objects.get(username=request.POST['battername'])
        except User.DoesNotExist:
            messages.error(request, '存在しないユーザー名を入力しています。修正してください。')
            return render(request, 'data.html')
        pitchername = Profile.objects.get(user=pitcher).name
        battername = Profile.objects.get(user=batter).name
        context = {
            'pitchername': pitchername,
            'battername': battername,
            'pitcher': pitcher,
            'batter': batter,
        }

        # ピッチャー・バッター名入力後もしくは打席結果入力後の、POST送信時
        if 'discrimination' not in request.POST:
            # 打席結果のPOST送信時の処理
            if 'contacted_results' in request.POST:
                contacted_results_form = ContactedResultsForm(request.POST)
                batting = Batting.objects.get(id=request.POST['batting_id'])
                if contacted_results_form.is_valid():
                    contacted_result = contacted_results_form.save(commit=False)
                    contacted_result.batting = batting
                    contacted_result.save()
                    messages.success(request, '打席最終結果の入力が完了しました。次の対戦選手名を入力してください。')
                    return redirect('data')
                else:
                    context.update({
                        'contacted_results_form': contacted_results_form,
                        'batting': batting,
                    })
                    messages.error(request, '不正な入力データがあります。修正してください。')
                    render(request, 'data.html', context)

            elif 'uncontacted_results' in request.POST:
                uncontacted_results_form = UncontactedResultsForm(request.POST)
                batting = Batting.objects.get(id=request.POST['batting_id'])
                if uncontacted_results_form.is_valid():
                    uncontacted_result = uncontacted_results_form.save(commit=False)
                    uncontacted_result.batting = batting
                    uncontacted_result.save()
                    messages.success(request, '打席最終結果の入力が完了しました。次の対戦選手名を入力してください。')
                    return redirect('data')
                else:
                    context.update({
                        'uncontacted_results_form': uncontacted_results_form,
                        'batting': batting
                    })
                    messages.error(request, '不正な入力データがあります。修正してください。')
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

        # シチュエーション以下各フォームへの入力後POST送信時(2回目以降)の共通処理
        else:
            situation_form = SituationForm(request.POST) # 入力データを引き継いでフォームに表示させる
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
                messages.success(request, '入力データを保存しました。')

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
                messages.error(request, '不正なデータ入力があります。修正してください。')

        return render(request, 'data.html', context)

    return render(request, 'data.html')

@login_required()
def statsview(request):
    if request.method == 'POST':
        try:
            player = User.objects.get(username=request.POST['playername'])
        except User.DoesNotExist:
            messages.error(request, '存在しないユーザー名を入力しています。修正してください。')
            return render(request, 'stats.html')
        contacted_scr = ContactedResults.objects.filter(score__gt=1). \
            filter(batting__user__id=player.id). \
            aggregate(Sum('score'))
        uncontacted_scr = UncontactedResults.objects.filter(score__gt=1). \
            filter(uncontacted_results__in=['base_on_ball', 'hit_by_pitch'])
        context = {
            'rbi': str(contacted_scr['score__sum']),
        }
        return render(request, 'stats.html', context)

    return render(request, 'stats.html')