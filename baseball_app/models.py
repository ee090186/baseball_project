from django.db import models
from django.contrib.auth.models import User
from django.db import models




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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name