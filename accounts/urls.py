from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('profile/', views.profileView, name='profile'),
    path('profile/update/', views.profileView_update, name='profile_update'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]