# Generated by Django 3.0.4 on 2020-09-29 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseball_app', '0008_auto_20200928_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='batting',
            name='discrimination',
            field=models.CharField(choices=[('undecided', '打席結果未定'), ('decided_with_contacted', '打席結果確定(フライアウト、ヒットなどバットとボールのコンタクト有り)'), ('decided_with_uncontacted', '打席結果確定(三振、四球などバットとボールのコンタクト無し)')], default='undecided', max_length=30, verbose_name='打席結果'),
            preserve_default=False,
        ),
    ]
