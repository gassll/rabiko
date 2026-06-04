from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            'username',
            'email'
        ]

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'settings-input',
                    'placeholder': 'Имя'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'settings-input',
                    'placeholder': 'Email'
                }
            ),

        }