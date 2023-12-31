from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Создайте пароль',
        'class' : 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Подтвердите пароль',
        'class' : 'form-control'
    }))
    class Meta:
        model = Account
        fields = {'first_name', 'last_name', 'phone_number', 'email', 'password'}


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Напишите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Напишите фамилию'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Напишите номер телефона'
        self.fields['email'].widget.attrs['placeholder'] = 'Эл-почта'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают!"
            )