from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Пароли не совпадают")

        return cleaned_data

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