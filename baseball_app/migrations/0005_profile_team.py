# Generated by Django 3.0.4 on 2020-09-21 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseball_app', '0004_auto_20200921_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='team',
            field=models.CharField(blank=True, max_length=100, verbose_name='チーム名'),
        ),
    ]
