# Generated by Django 3.0.4 on 2020-09-28 01:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('baseball_app', '0007_auto_20200922_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batting', models.CharField(choices=[('swing_and_missed', '空振り'), ('swing_and_contact', 'ゴロ・フライ・ライナー・単打・長打'), ('foul', 'ファール'), ('taken', '見送り'), ('other', 'その他')], max_length=20, verbose_name='打者の行動')),
            ],
        ),
        migrations.CreateModel(
            name='Situation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(choices=[('0', 'ランナーなし'), ('1', '1塁'), ('2', '2塁'), ('3', '3塁'), ('1-2', '1塁2塁'), ('1-3', '1塁3塁'), ('2-3', '2塁3塁'), ('1-2-3', '満塁')], max_length=20, verbose_name='出塁状況')),
                ('outs', models.CharField(choices=[('0', '0アウト'), ('1', '1アウト'), ('2', '2アウト')], max_length=20, verbose_name='アウトカウント')),
                ('ball_count', models.CharField(choices=[('0', '0ボール'), ('1', '1ボール'), ('2', '2ボール'), ('3', '3ボール')], max_length=20, verbose_name='ボール')),
                ('strike_count', models.CharField(choices=[('0', '0ストライク'), ('1', '1ストライク'), ('2', '2ストライク')], max_length=20, verbose_name='ストライク')),
                ('inning', models.CharField(choices=[('1', '1回'), ('2', '2回'), ('3', '3回'), ('4', '4回'), ('5', '5回'), ('6', '6回'), ('7', '7回'), ('8', '8回'), ('9', '9回'), ('10', '10回'), ('11', '11回'), ('12', '12回以上')], max_length=20, verbose_name='回')),
            ],
        ),
        migrations.CreateModel(
            name='UncontactedResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uncontacted_results', models.CharField(choices=[('strikeout', '三振'), ('base_on_ball', '四球'), ('wild_pit', 'ワイルドピッチ'), ('passed_ball', 'パスボール'), ('hit_by_pitch', '死球')], max_length=20, verbose_name='結果')),
                ('score', models.IntegerField(blank=True, null=True, verbose_name='得点')),
                ('added_number_of_outs', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=20, verbose_name='増えたアウトカウント')),
                ('batting', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='baseball_app.Batting')),
            ],
        ),
        migrations.CreateModel(
            name='Pitting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('side_corse', models.CharField(choices=[('inside', '内角'), ('near_inside', '内角寄り'), ('middle', '真ん中'), ('near_outside', '外角寄り'), ('outside', '外角')], max_length=20, verbose_name='左右のコース')),
                ('height_corse', models.CharField(choices=[('low', '低め'), ('near_low', '低め寄り'), ('middle', '真ん中'), ('near_high', '高め寄り'), ('high', '高め')], max_length=20, verbose_name='上下のコース')),
                ('speed', models.CharField(choices=[('100', '100km以下'), ('110', '110km台'), ('120', '120km台'), ('130', '130km台'), ('140', '140km台'), ('150', '150km台'), ('160', '160km以上')], max_length=20, verbose_name='球速')),
                ('type_of_pitch', models.CharField(choices=[('4sfb', 'ストレート'), ('cb', 'カーブ'), ('sl', 'スライダー'), ('frk', 'フォーク'), ('cut', 'カットボール'), ('scr', 'スクリュー'), ('ch', 'チェンジアップ'), ('kn', 'ナックル'), ('2sfb', 'ツーシーム'), ('rfb', 'シュート')], max_length=20, verbose_name='球種')),
                ('pichout_or_waste', models.BooleanField(default=False, verbose_name='ピッチアウト,捨て球')),
                ('bark', models.BooleanField(default=False, verbose_name='ボーク')),
                ('number_of_pitches', models.IntegerField(verbose_name='球数')),
                ('situation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='baseball_app.Situation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContactedResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contacted_results', models.CharField(choices=[('groundball', 'ゴロ'), ('flyball', 'フライ'), ('linedrive', 'ライナー'), ('single', '単打'), ('double', '2塁打'), ('triple', '3塁打'), ('inside_the_park_homerun', 'ランニングホームラン'), ('homerun', 'ホームラン')], max_length=30, verbose_name='結果')),
                ('catch_position_choices', models.CharField(choices=[('picher', 'ピッチャー'), ('catcher', 'キャッチャー'), ('first', 'ファースト'), ('second', 'セカンド'), ('third', 'サード'), ('short', 'ショート'), ('left', 'レフト'), ('center', 'センター'), ('right', 'ライト')], max_length=30, verbose_name='打球方向')),
                ('score', models.IntegerField(blank=True, null=True, verbose_name='得点')),
                ('added_number_of_outs', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=20, verbose_name='増えたアウトカウント')),
                ('batting', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='baseball_app.Batting')),
            ],
        ),
        migrations.AddField(
            model_name='batting',
            name='pitting',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='baseball_app.Pitting'),
        ),
        migrations.AddField(
            model_name='batting',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
