from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from django.db.models.fields import BooleanField, IntegerField


class Profile(models.Model):
    GENDER_CHOICES = (
        ('man', '男性'),
        ('woman', '女性'),
        ('other', 'その他'),
    )

    POSITION_CHOICES = (
        ('picher', 'ピッチャー'),
        ('catcher', 'キャッチャー'),
        ('first', 'ファースト'),
        ('second', 'セカンド'),
        ('third', 'サード'),
        ('short', 'ショート'),
        ('left', 'レフト'),
        ('center', 'センター'),
        ('right', 'ライト'),
    )

    BATTING_HANDEDNESS_CHOICES = (
        ('right_handed_batting', '右打ち'),
        ('left_handed_batting', '左打ち'),
        ('switch_hitter', '両打ち'),
    )

    THROWING_HANDEDNESS_CHOICES = (
        ('right_handed_throwing', '右投げ'),
        ('left_handed_throwing', '左投げ'),
        ('switch_picher', '両投げ'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('氏名', max_length=100)
    gender = models.CharField('性別', max_length=5, choices=GENDER_CHOICES)
    birthday = models.DateField('生年月日', blank=True)
    email = models.EmailField('メールアドレス', blank=True)
    height = models.FloatField('身長', blank=True)
    weight = models.FloatField('体重', blank=True)
    uniform_number = models.IntegerField('背番号', blank=True)
    position = models.CharField('ポジション', max_length=7, choices=POSITION_CHOICES)
    batting_handedness = models.CharField('打ち方', max_length=20, choices=BATTING_HANDEDNESS_CHOICES)
    throwing_handedness = models.CharField('投げ方', max_length=21, choices=THROWING_HANDEDNESS_CHOICES)
    team = models.CharField('チーム名', max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name



class Situation(models.Model):
    BASE_CHOICES = (
        ('0', 'ランナーなし'),
        ('1', '1塁'),
        ('2', '2塁'),
        ('3', '3塁'),
        ('1-2', '1塁2塁'),
        ('1-3', '1塁3塁'),
        ('2-3', '2塁3塁'),
        ('1-2-3', '満塁'),
    )

    OUTS_CHOICES = (
        ('0', '0アウト'),
        ('1', '1アウト'),
        ('2', '2アウト'),
    )

    BAll_COUNT_CHOICES = (
        ('0', '0ボール'),
        ('1', '1ボール'),
        ('2', '2ボール'),
        ('3', '3ボール'),
    )

    STRIKE_COUNT_CHOICES = (
        ('0', '0ストライク'),
        ('1', '1ストライク'),
        ('2', '2ストライク'),
    )

    INNING_CHOICES = (
        ('1', '1回'),
        ('2', '2回'),
        ('3', '3回'),
        ('4', '4回'),
        ('5', '5回'),
        ('6', '6回'),
        ('7', '7回'),
        ('8', '8回'),
        ('9', '9回'),
        ('10', '10回'),
        ('11', '11回'),
        ('12', '12回以上'),
    )
    base = models.CharField('出塁状況', max_length=20, choices=BASE_CHOICES)
    outs = models.CharField('アウトカウント', max_length=20, choices=OUTS_CHOICES)
    ball_count = models.CharField('ボール', max_length=20, choices=BAll_COUNT_CHOICES)
    strike_count = models.CharField('ストライク', max_length=20, choices=STRIKE_COUNT_CHOICES)
    inning = models.CharField('回', max_length=20, choices=INNING_CHOICES)
    def __str__(self):
        return self.inning + '(' + self.outs + ')'



class Pitting(models.Model):
    SIDE_COURSE_CHOICES = (
        ('inside', '内角'),
        ('near_inside', '内角寄り'),
        ('middle', '真ん中'),
        ('near_outside', '外角寄り'),
        ('outside', '外角'),
    )

    HEIGHT_COURSE_CHOICES = (
        ('low', '低め'),
        ('near_low', '低め寄り'),
        ('middle', '真ん中'),
        ('near_high', '高め寄り'),
        ('high', '高め'),
    )

    SPEED_CHOICES = (
        ('100', '100km以下'),
        ('110', '110km台'),
        ('120', '120km台'),
        ('130', '130km台'),
        ('140', '140km台'),
        ('150', '150km台'),
        ('160', '160km以上'),
    )

    TYPE_OF_PITCH_CHOICES = (
        ('4sfb', 'ストレート'),
        ('cb', 'カーブ'),
        ('sl', 'スライダー'),
        ('frk', 'フォーク'),
        ('cut', 'カットボール'),
        ('scr', 'スクリュー'),
        ('ch', 'チェンジアップ'),
        ('kn', 'ナックル'),
        ('2sfb', 'ツーシーム'),
        ('rfb', 'シュート'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    situation = models.OneToOneField(Situation, on_delete=models.CASCADE)
    side_corse = models.CharField('左右のコース', max_length=20, choices=SIDE_COURSE_CHOICES)
    height_corse = models.CharField('上下のコース', max_length=20, choices=HEIGHT_COURSE_CHOICES)
    speed = models.CharField('球速', max_length=20, choices=SPEED_CHOICES)
    type_of_pitch = models.CharField('球種', max_length=20, choices=TYPE_OF_PITCH_CHOICES)
    pichout_or_waste = models.BooleanField('ピッチアウト,捨て球', default=False)
    bark = models.BooleanField('ボーク', default=False)
    number_of_pitches = models.IntegerField('球数')
    def __str__(self):
        return str(self.user) + '(' + self.number_of_pitches + ')'



class Batting(models.Model):
    BATTING_CHOICES = (
        ('swing_and_missed', '空振り'),
        ('swing_and_contact', 'ゴロ・フライ・ライナー・単打・長打'),
        ('foul', 'ファール'),
        ('taken', '見送り'),
        ('other', 'その他'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pitting = models.OneToOneField(Pitting, on_delete=models.CASCADE)
    batting = models.CharField('打者の行動', max_length=20, choices=BATTING_CHOICES)
    def __str__(self):
        return str(self.user) + self.batting



class ContactedResults(models.Model):
    CONTACTED_RESULTS_CHOICES = (
        ('groundball', 'ゴロ'),
        ('flyball', 'フライ'),
        ('linedrive', 'ライナー'),
        ('single', '単打'),
        ('double', '2塁打'),
        ('triple', '3塁打'),
        ('inside_the_park_homerun', 'ランニングホームラン'),
        ('homerun', 'ホームラン'),
    )
    CATCH_POSITION_CHOICES = (
        ('picher', 'ピッチャー'),
        ('catcher', 'キャッチャー'),
        ('first', 'ファースト'),
        ('second', 'セカンド'),
        ('third', 'サード'),
        ('short', 'ショート'),
        ('left', 'レフト'),
        ('center', 'センター'),
        ('right', 'ライト'),
    )
    ADDED_NUMBER_OF_OUTS_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    batting = models.OneToOneField(Batting, on_delete=CASCADE)
    contacted_results = models.CharField('結果', max_length=20,choices=CONTACTED_RESULTS_CHOICES)
    catch_position_choices = models.CharField('打球方向', max_length=20, choices=CATCH_POSITION_CHOICES)
    score = models.IntegerField('得点', blank=True, null=True)
    added_number_of_outs = models.CharField('増えたアウトカウント', max_length=20, choices=ADDED_NUMBER_OF_OUTS_CHOICES)
    def __str__(self):
        return str(self.contacted_results)



class UncontactedResults(models.Model):
    UNCONTACTED_RESULTS_CHOICES = (
        ('strikeout', '三振'),
        ('base_on_ball', '四球'),
        ('wild_pit', 'ワイルドピッチ'),
        ('passed_ball', 'パスボール'),
        ('hit_by_pitch', '死球'),
    )
    ADDED_NUMBER_OF_OUTS_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    batting = models.OneToOneField(Batting, on_delete=models.CASCADE)
    uncontacted_results = models.CharField('結果', max_length=20, choices=UNCONTACTED_RESULTS_CHOICES)
    score = models.IntegerField('得点', blank=True, null=True)
    added_number_of_outs = models.CharField('増えたアウトカウント', max_length=20, choices=ADDED_NUMBER_OF_OUTS_CHOICES)
    def __str__(self):
        return str(self.uncontacted_results)

