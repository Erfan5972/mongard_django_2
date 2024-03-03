from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('reset/', views.UserResetPasswordView.as_view(), name='reset_password'),
    path('reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/confirm/<uidb64>/token/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]