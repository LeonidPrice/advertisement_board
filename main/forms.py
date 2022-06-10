from dataclasses import fields
from django import forms
from django.urls import reverse_lazy
from .models import AdvUser
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .apps import user_registered


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')

class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адресс электронной почты')
    password_1 = forms.CharField(label='Пароль', 
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html())
    password_2 = forms.CharField(label='Пароль (повторно)',
        widget=forms.PasswordInput,
        help_text='Введите пароль повторно для проверки')
        # поля формы входа

    def clean_password_1(self):
        password_1 = self.cleaned_data['password_1']
        if password_1:
            password_validation.validate_password(password_1)
        return password_1
        # валидация пароля

    def clean(self):
        super().clean()
        password_1 = self.cleaned_data['password_1']
        password_2 = self.cleaned_data['password_2']
        if password_1 and password_2 and password_1 != password_2:
            errors = {'password_2': 
                ValidationError('Введенные пароли не совпадают', 
                code='password_mismatch')}
            raise ValidationError(errors)
        # проверка совпадения двух паролей

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email',
            'password_1', 'password_2',
            'first_name', 'last_name', 'send_messages')

