from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



def email_validator(email):
    emails = [u.email for u in User.objects.all()]
    error = False
    if email in emails:
        error = True
    if error:
        raise ValidationError('Пользователь с таким e-mail адресом уже существует')
    return email



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control',}))
    email = forms.EmailField(label='e-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off',}),
                             validators=[email_validator,])
    password1 = forms.CharField(label='Придумайте пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',}))
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',}))

    class Meta:
        model = User
        fields = 'username', 'email', 'password1', 'password2',





class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Введите имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',}))


class UserLoginFormNavbar(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
