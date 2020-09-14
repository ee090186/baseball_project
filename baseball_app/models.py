from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.db import models


GENDER_CHOICES = (
    ('1', '女性'),
    ('2', '男性'),
)


class Profile(models.Model):
    name = models.CharField('ハンドルネーム', max_length=255)
    phone = models.CharField('電話番号', max_length=255, blank=True)
    gender = models.CharField('性別', max_length=2, choices=GENDER_CHOICES, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name