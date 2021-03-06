# Generated by Django 3.0.4 on 2020-09-15 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseball_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone',
        ),
        migrations.AddField(
            model_name='profile',
            name='batting_handedness',
            field=models.CharField(choices=[('right_handed_batting', '右打ち'), ('left_handed_batting', '左打ち'), ('switch_hitter', '両打ち')], default='right_handed_batting', max_length=20, verbose_name='打ち方'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, default='1990-01-01', verbose_name='生年月日'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='メールアドレス'),
        ),
        migrations.AddField(
            model_name='profile',
            name='height',
            field=models.FloatField(blank=True, default=170.0, verbose_name='身長'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='position',
            field=models.CharField(choices=[('picher', 'ピッチャー'), ('catcher', 'キャッチャー'), ('first', 'ファースト'), ('second', 'セカンド'), ('third', 'サード'), ('short', 'ショート'), ('left', 'レフト'), ('center', 'センター'), ('right', 'ライト')], default='picher', max_length=7, verbose_name='ポジション'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='throwing_handedness',
            field=models.CharField(choices=[('right_handed_throwing', '右投げ'), ('left_handed_throwing', '左投げ'), ('switch_picher', '両投げ')], default='right_handed_throwing', max_length=21, verbose_name='投げ方'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='uniform_number',
            field=models.IntegerField(blank=True, default=1, verbose_name='背番号'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='weight',
            field=models.FloatField(blank=True, default=60.0, verbose_name='体重'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.IntegerField(choices=[('man', '女性'), ('woman', '男性'), ('other', 'その他')], verbose_name='性別'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=100, verbose_name='氏名'),
        ),
    ]
