from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify/<str:token>/', verify_email, name='verify_email'),
    path('check_email/', CheckEmailView.as_view(), name='check_email'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('top-up/', top_up_balance, name='top-up'),
]