
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
import uuid

CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    user_image = forms.ImageField(label='Аватар пользователя',widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.verification_token = str(uuid.uuid4())
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_image', 'password1', 'password2')




class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    user_image = forms.ImageField(label='Аватар пользователя',widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_image')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'password')


# class CustomUserChangeFormAdmin(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'money', 'user_image', 'tag', 'is_email_verified')


class TopUpForm(forms.Form):
    card_number = forms.IntegerField(label='Номер карты',widget=forms.NumberInput(attrs={'class': 'form-control'}))
    card_date = forms.DateField(
        label='Дата годности карты',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0, label='Сумма пополнения', widget=forms.NumberInput(attrs={'class': 'form-control'}))