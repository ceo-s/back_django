from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models

class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class": "intro-form"}))
    telegram = forms.CharField(label="Telegram", widget=forms.TextInput(attrs={"class": "intro-form"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "intro-form"}))
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(attrs={"class": "intro-form"}))
    class Meta:
        model = models.TgUser
        fields = ["username", "telegram", "password1", "password2"]
        