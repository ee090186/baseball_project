from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from .models import Profile


class UserCreateForm(UserCreationForm):
    username = forms.CharField(label='名前', \
        widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='パスワード', \
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='パスワード(再確認)', \
        widget=forms.PasswordInput(attrs={'class':'form-control'}))



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "name", "gender", "phone"
        )