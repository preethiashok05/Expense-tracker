from django.urls import path
from .views import ForgotPassword, ResetPassword, UsernameView , EmailView ,RegistrationView, VerificationView,LoginView,LogoutView,ForgotPassword,ConfirmView,CheckView, ChangePassword;
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
     path('register',RegistrationView.as_view(), name="register"),
     path('',LoginView.as_view(), name="login"),
     path('logout', LogoutView.as_view(), name="logout"),
     path('validate-username', csrf_exempt(UsernameView.as_view()), name="validate-username"),    
     path('validate-email', csrf_exempt(EmailView.as_view()),  name='validate-email'),       
     path('activate/<uidb64>/<token>', VerificationView.as_view(), name="activate"),

     #------------------------------------ Forgot password -----------------------
     path('change-password',ChangePassword.as_view() , name="change-password" ),
     path('password-reset-form',ForgotPassword.as_view(), name="password-reset-form"),
     path('password-change-confirm',CheckView.as_view(), name="password"),
     path('confirm/<uidb64>/<token>',ConfirmView.as_view(), name="confirm"),
     path('reset-password' , ResetPassword.as_view() , name='reset-password')
    
]