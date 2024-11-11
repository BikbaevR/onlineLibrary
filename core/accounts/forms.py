
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_image')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_image')
        exclude = ['password']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


# class CustomUserChangeFormAdmin(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'money', 'user_image', 'tag', 'is_email_verified')


class TopUpForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0, label='Сумма пополнения')