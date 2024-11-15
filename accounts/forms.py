from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=60, required=True, help_text='Required')
    last_name = forms.CharField(max_length=60, required=True, help_text='Required')

    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('username', 'first_name', 'last_name', 'email')
        
    def __init__(self, *args, **kwargs): # Remove help text to inputs.
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None


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

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
    )