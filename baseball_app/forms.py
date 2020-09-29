from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.forms import widgets
from .models import Profile, Situation, Pitting, Batting, ContactedResults, UncontactedResults


class UserCreateForm(UserCreationForm):
    username = forms.CharField(label='名前', \
        widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='パスワード', \
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='パスワード(再確認)', \
        widget=forms.PasswordInput(attrs={'class':'form-control'}))


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Profile
        fields = (
            "name", "gender", "birthday", "email", "height", "weight", "uniform_number", "position", "batting_handedness", "throwing_handedness", "team"
        )
        

class SituationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Situation
        fields = (
            'base', 'outs', 'ball_count', 'strike_count', 'inning'
        )


class PittingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Pitting
        fields = (
            'side_corse', 'height_corse', 'speed', 'type_of_pitch', 'pichout_or_waste', 'bark', 'number_of_pitches',
        )


class BattingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Batting
        fields = (
            'batting', 'discrimination'
        )


class ContactedResultsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = ContactedResults
        fields = (
            'contacted_results', 'catch_position_choices', 'score', 'added_number_of_outs'
        )


class UncontactedResultsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = UncontactedResults
        fields = (
            'uncontacted_results', 'score', 'added_number_of_outs'
        )

