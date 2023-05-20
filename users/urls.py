from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (UserRegisterView, UsersConfirmationView, UsersLoginView,
                    UsersUpdateView)

app_name = 'app_users'

urlpatterns = [
    path('login/', UsersLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', UsersUpdateView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('confirm-email/<uuid:code>/', UsersConfirmationView.as_view(), name='confirm'),
]
