from django.urls import path
from .views import UsernameAvailable, CompanyUserView, LoginView, LogoutView, RefreshTokenView

urlpatterns = [
    path('is-username-available/',UsernameAvailable.as_view(), name='is-username-available'),
    path('register/',CompanyUserView.as_view(), name='register'),
    path('login/',LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('refresh-token/',RefreshTokenView.as_view(), name='refresh-token'),
]