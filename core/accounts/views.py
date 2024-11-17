from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.urls import reverse
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView, ListView
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm, TopUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from library.models import TopUpHistory

CustomUser = get_user_model()


def verify_email(request, token):
    user = get_object_or_404(CustomUser, verification_token=token)
    user.is_email_verified = True
    user.verification_token = ''
    user.save()
    return redirect('index')


def email_verified_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_email_verified:
            return redirect(reverse('check_email'))
        return function(request, *args, **kwargs)
    return wrap


class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST, request.FILES)
        print(1)
        if form.is_valid():
            print(2)
            user = form.save()
            verification_url = request.build_absolute_uri(f'/accounts/verify/{user.verification_token}/')
            send_mail(
                'Подтверждение email',
                f'Для подтверждения вашего email перейдите по ссылке: {verification_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            return redirect('check_email')
        else:
            print(form.errors)
        return render(request, self.template_name, {'form': form})


class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            print(form.errors)
        return render(request, self.template_name, {'form': form})


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    # @login_required
    def get(self, request, *args, **kwargs):

        user = CustomUser.objects.get(username=request.user.username)

        form = CustomUserChangeForm(instance=request.user)
        return render(request, self.template_name, {'form': form, 'user': user})

    # @login_required
    def post(self, request, *args, **kwargs):
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


class CheckEmailView(TemplateView):
    template_name = 'accounts/check_email.html'


class LogoutUserView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


class TopUpBalanceView(LoginRequiredMixin, View):
    template_name = 'accounts/top_up_balance.html'

    def get(self, request, *args, **kwargs):
        form = TopUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            card_number = form.cleaned_data.get('card_number', None)
            request.user.money += amount
            request.user.save()

            TopUpHistory.objects.create(
                user=request.user,
                card_number=card_number,
                datetime=now(),
                amount=amount,
            )

            return redirect('profile')

        return render(request, self.template_name, {'form': form})


class TopUpHistoryView(LoginRequiredMixin, ListView):
    model = TopUpHistory
    template_name = 'accounts/top_up_history.html'
    context_object_name = 'history'

    def get_queryset(self):
        return TopUpHistory.objects.filter(user=self.request.user).order_by('-datetime')