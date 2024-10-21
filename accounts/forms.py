from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=60, required=True, help_text='Required')
    last_name = forms.CharField(max_length=60, required=True, help_text='Required')

    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('username', 'first_name', 'last_name', 'email')


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(max_length=60, required=True, help_text='Required')
    last_name = forms.CharField(max_length=60, required=True, help_text='Required')
    street_address = forms.CharField(max_length=255, required=False, help_text='Optional')
    city = forms.CharField(max_length=100, required=False, help_text='Optional')
    state = forms.CharField(max_length=100, required=False, help_text='Optional')
    zip_code = forms.CharField(max_length=20, required=False, help_text='Optional')
    country = forms.CharField(max_length=100, required=False, help_text='Optional')
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text='Leave blank if not changing')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'street_address', 'city', 'state', 'zip_code', 'country']

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password == "":
            return None
        return password
