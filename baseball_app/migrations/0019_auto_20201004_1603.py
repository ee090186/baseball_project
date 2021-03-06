# Generated by Django 3.0.4 on 2020-10-04 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseball_app', '0018_auto_20201004_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='position',
            field=models.CharField(choices=[('pitcher', 'ピッチャー'), ('catcher', 'キャッチャー'), ('first', 'ファースト'), ('second', 'セカンド'), ('third', 'サード'), ('short', 'ショート'), ('left', 'レフト'), ('center', 'センター'), ('right', 'ライト')], max_length=7, verbose_name='ポジション（必須）'),
        ),
    ]
