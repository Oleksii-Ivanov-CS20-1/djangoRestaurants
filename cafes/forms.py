from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from cafes.models import CustomUser, Record
from .models import Reviews, RatingStar, Rating


class ReviewForms(forms.ModelForm):
    """Form reviews"""

    class Meta:
        model = Reviews
        fields = ("name", "email", "text")


class RatingForm(forms.ModelForm):
    """Rating form"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(),
        widget=forms.RadioSelect(),
        empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ["name", "street", "phone", "types", "category", "mainPhoto", "description", "url"]
