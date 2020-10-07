from django.db.models import aggregates
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
            messages.error(request, '有効でない入力があります。修正してください。')

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
            messages.error(request, '有効でないデータを入力しています。修正してください。')

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
                batting = Batting.objects.get(id=request.POST['batting_id'])
                contacted_results_form = ContactedResultsForm(request.POST)
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
                    messages.error(request, '有効でない入力データがあります。修正してください。')
                    render(request, 'data.html', context)

            elif 'uncontacted_results' in request.POST:
                batting = Batting.objects.get(id=request.POST['batting_id'])
                uncontacted_results_form = UncontactedResultsForm(request.POST)
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
                    messages.error(request, '有効でない入力データがあります。修正してください。')
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
                

                # 打席結果未定時のフォーム準備
                if request.POST['discrimination'] == 'undecided':
                    context.update({
                        'situation_form': situation_form,
                        'pitting_form': pitting_form,
                        'batting_form': batting_form,
                        })
                    messages.success(request, '入力データを保存しました。')

                # 以下二つの条件分岐は、打席結果確定時のフォーム準備・データ保存
                elif request.POST['discrimination'] == 'decided_with_contacted':
                    contacted_results_form = ContactedResultsForm()
                    context.update({
                        'contacted_results_form': contacted_results_form,
                        'batting': batting, # 打席結果保存する際に、該当するbattingと紐づけるため一緒に送る
                        })
                    messages.success(request, '入力データを保存しました。打席最終結果詳細を入力して送信してください。')
                elif request.POST['discrimination'] == 'decided_with_uncontacted':
                    uncontacted_results_form = UncontactedResultsForm()
                    context.update({
                        'uncontacted_results_form': uncontacted_results_form,
                        'batting': batting, 
                        })
                    messages.success(request, '入力データを保存しました。打席最終結果詳細を入力して送信してください。')
            # 入力が有効でなかった場合
            else:
                context.update({
                    'situation_form': situation_form,
                    'pitting_form': pitting_form,
                    'batting_form': batting_form,
                    })
                messages.error(request, '有効でない入力データがあります。修正してください。')

        return render(request, 'data.html', context)

    return render(request, 'data.html')



@login_required()
def statsview(request):
    if request.method == 'POST':
        # ユーザー名のバリデーション
        try:
            player = User.objects.get(username=request.POST['playername'])
        except User.DoesNotExist:
            messages.error(request, '存在しないユーザー名を入力しています。修正してください。')
            return render(request, 'stats.html')

        # 打点
        contacted_scr = ContactedResults.objects.filter(score__gte=1). \
                        filter(batting__user__id=player.id). \
                        aggregate(Sum('score'))
        uncontacted_scr = UncontactedResults.objects.filter(
                            score__gte=1,
                            uncontacted_results__in=['base_on_ball', 'hit_by_pitch'],
                            batting__user__id=player.id
                            ). \
                            aggregate(Sum('score'))
        
        runs_batted_in = sum(transnone_to_zero(contacted_scr['score__sum'], uncontacted_scr['score__sum'])) # エラー線原因不明。

        # 打率
        contacted_qset = ContactedResults.objects.filter(batting__user__id=player.id)
        contacted_at_bat = contacted_qset.count()
        sac_qset = contacted_qset.filter(batting__batting='sacrifice')
        num_of_sac = sac_qset.count() # 犠打数
        uncontacted_qset = UncontactedResults.objects.filter(batting__user__id=player.id)
        num_of_strikeout = uncontacted_qset.filter(uncontacted_results='strikeout').count() # 三振数
        num_of_bob_and_hbp = uncontacted_qset.filter(uncontacted_results__in=
                            ['base_on_ball', 'hit_by_pitch']).count() # 四死球数
        uncontacted_at_bat = num_of_strikeout
        at_but = contacted_at_bat + uncontacted_at_bat - num_of_sac # 打数（＝打席数－四死球－犠打）
        hit_qset = contacted_qset.exclude(contacted_results__in=
                    ['groundball', 'flyball', 'linedrive'])
        num_of_hits = hit_qset.count() # 安打数
        try:
            batting_average = round(num_of_hits / at_but, 5) * 10
        except ZeroDivisionError:
            batting_average = '算出するにはデータが足りません'

        # 本塁打数
        num_of_homerun = ContactedResults.objects.filter(contacted_results__in=
                        ['inside_the_park_homerun','homerun'],
                        batting__user__id=player.id).count()

        # 長打率
        num_of_single = hit_qset.filter(contacted_results='single').count()
        num_of_double = hit_qset.filter(contacted_results='double').count()
        num_of_triple = hit_qset.filter(contacted_results='triple').count()
        try:
            slugging_average = round((num_of_single + num_of_double*2 +
                               num_of_triple*3 + num_of_homerun*4)/ at_but, 3)
        except ZeroDivisionError:
            slugging_average = '算出するにはデータが足りません'

        # 出塁率
        num_of_sacfly = sac_qset.filter(contacted_results='flyball').count() # 犠牲フライ数
        try:
            on_base_percentage = round((num_of_hits + num_of_bob_and_hbp) 
                                / (at_but + num_of_bob_and_hbp + num_of_sacfly), 3)
        except ZeroDivisionError:
            on_base_percentage = '算出するにはデータが足りません'

        context = {
            'player': player,
            'batting_aberage': batting_average,
            'runs_batted_in': runs_batted_in,
            'num_of_homerun': num_of_homerun,
            'on_base_percentage': on_base_percentage,
            'slugging_average': slugging_average,
        }
        
        # playerのpositionがpitcherの場合、投手用の指標を準備
        if Profile.objects.get(user=player).position == 'pitcher':
            pitcher_dstct = True
            # 失点率
            contacted_qset = ContactedResults.objects.filter(batting__pitting__user=player)
            cnt_num_of_outs = contacted_qset.aggregate(Sum('added_number_of_outs')) # 獲得アウト数1
            contacted_runs = contacted_qset.filter(score__gte=1).aggregate(Sum('score')) # 失点数1
            uncontacted_qset = UncontactedResults.objects.filter(batting__pitting__user=player)
            uct_num_of_outs = uncontacted_qset.aggregate(Sum('added_number_of_outs')) # 獲得アウト数2
            uncontacted_runs = uncontacted_qset.filter(score__gte=1).aggregate(Sum('score')) # 失点数2
            num_of_outs = sum(transnone_to_zero(
                cnt_num_of_outs['added_number_of_outs__sum'],
                uct_num_of_outs['added_number_of_outs__sum'])) # 獲得アウト数合計
            earned_runs = sum(transnone_to_zero(
                contacted_runs['score__sum'],
                uncontacted_runs['score__sum'])) # 失点数（自責点の概念を無視する）
            try:
                run_average = earned_runs / (num_of_outs / 27) # 失点率
            except ZeroDivisionError:
                run_average = '算出するにはデータが足りません'

            # 奪三振率
            cnt_batsman_faced = contacted_qset.count() # 打席数1
            uct_batsman_faced = uncontacted_qset.count() # 打席数2
            batsman_faced = cnt_batsman_faced + uct_batsman_faced # 打席数合計
            num_of_strikeout = uncontacted_qset.filter(
                               uncontacted_results='strikeout').count() # 奪三振数
            try:
                k_percentage = round(num_of_strikeout / batsman_faced, 3)
            except ZeroDivisionError:
                k_percentage = '算出するにはデータが足りません'

            # 被本塁打率
            earned_hr = contacted_qset.filter(contacted_results__in=
                            ['homerun', 'inside_the_park_homerun']).count() # 被本塁打数
            try:
                hr_per_9 = round(earned_hr/batsman_faced, 3)
            except ZeroDivisionError:
                hr_per_9 = '算出するにはデータが足りません'

            # 与四球率
            num_of_bb = uncontacted_qset.filter(uncontacted_results='base_on_ball').count() # 四球数
            try:
                bb_percentage = round(num_of_bb / batsman_faced, 3)
            except ZeroDivisionError:
                bb_percentage = '算出するにはデータが足りません'

            # K-BB%
            try:
                k_bb_percentage = round((num_of_strikeout - num_of_bb)/batsman_faced, 3) # (奪三振数－四球数)/打席数
            except ZeroDivisionError:
                k_bb_percentage = '算出するにはデータが足りません'

            context.update({
                'pitcher_dstct': pitcher_dstct,
                'run_average': run_average,
                'k_percentage': k_percentage,
                'hr_per_9': hr_per_9,
                'bb_percentage': bb_percentage,
                'k_bb_percentage': k_bb_percentage,
                })
        
        return render(request, 'stats.html', context)

    return render(request, 'stats.html')



def transnone_to_zero(*args):
    if len(args) >= 2:
        lst = []
        for obj in args:
            if obj == None:
                lst.append(0) 
            else:
                lst.append(obj)
        return lst

    else:
        if args == None:
            return 0
        
        return args


