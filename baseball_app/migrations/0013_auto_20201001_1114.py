# Generated by Django 3.0.4 on 2020-10-01 02:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseball_app', '0012_auto_20201001_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uniform_number',
            field=models.PositiveIntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999)], verbose_name='背番号'),
        ),
    ]
