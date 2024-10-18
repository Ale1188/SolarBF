from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.models import AbstractUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=60, required=True, help_text='Required')
    last_name = forms.CharField(max_length=60, required=True, help_text='Required')

    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('username', 'first_name', 'last_name', 'email')


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(max_length=60, required=True, help_text='Required')
    last_name = forms.CharField(max_length=60, required=True, help_text='Required')
    address = forms.CharField(max_length=255, required=False, help_text='Optional')
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text='Leave blank if not changing')

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'address')

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password == "":
            return None
        return password