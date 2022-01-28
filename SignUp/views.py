from curses.ascii import isalnum
from django.shortcuts import render ,redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.contrib import messages , auth
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import account_activation_token
from django.urls import reverse
import json
#User.objects.all().delete()


class UsernameView(View):
    def post(self, request):
        print(f"request sent is {request}")
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_sucmessages.success': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_sucmessages.success': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})
    
class EmailView(View):
    def post(self, request):
        print(request)
        data = json.loads(request.body)
        email = data['email']
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_sucmessages.success': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})
        
class RegistrationView(View):
    def get(self, request):
        return render(request, 'signup/form.html')
    
    def post(self , request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context ={
             'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.success(request, 'Password too short')
                    return render(request, 'signup/form.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                print(f"user pk = {user.pk}")

                current_site = get_current_site(request)

                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})
                print(f"uid = {email_body['uid']}")

                email_subject = 'Activate your account'

                activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created')
                return render(request, 'signup/form.html')
        return render(request, 'signup/form.html')

class VerificationView(View):
     def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
        
            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')

class LoginView(View):
    def get(self ,request):
        return render(request , 'signup/login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request,user)
                    print(user)
                    messages.success(request, 'Logged in  Successfully')
                    return redirect('/expenses/')
                
                messages.success(request , 'Account not activated , please check the activation link sent to your email')
                return render(request ,'signup/login.html')
            
            messages.success(request ,'Username or Pssword is incorrect , Please try again')
            return render(request ,'signup/login.html')   

        messages.success(request, 'Please fill all the fields')
        return render(request ,'signup/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')


# ------------------------------------------------------RESET PASSWORD ----------------------------------------------
class ForgotPassword(View):
    def get(self, request):
        return render(request,'registration/password_reset_form.html')

class CheckView(View):
    def get(self, request):
        return render(request, 'registration/password_reset_form.html')
    def post(self , request):
        email = request.POST['email']
        print(email)  
        if User.objects.filter(email=email).exists():
            current_site = get_current_site(request)
            user = User.objects.get(email=email)
            email_body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            link = reverse('confirm', kwargs={
                            'uidb64': email_body['uid'], 'token': email_body['token']})
            print(f"uid = {email_body['uid']}")

            email_subject = 'Reset Password'

            activate_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                'Hi '+user.username + ', Please click the link below to reset your password \n'+activate_url,
                'noreply@semycolon.com',
                [email],
            )
            email.send(fail_silently=False)
            messages.success(request, 'check your mail to reset password')
            return render(request, 'registration/password_reset_form.html')

        messages.error('No user exists with this email')
        return render(request, 'registration/password_reset_form.html')

class ConfirmView(View):
    def get(self, request, uidb64, token):
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        if user.is_active:
            return redirect('change-password') 
        
        return redirect('password-reset-form')


class ChangePassword(View):
    def get(self, request):
        return render(request,'registration/password_reset_confirm.html')

class ResetPassword(View):
    def get(self ,request):
        return render(request,'registration/password_reset_confirm.html')
    def post(self , request):
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not password1 == password2:
            messages.error(request,'Passwords dont match')
            return render(request , 'registration/password_reset_confirm.html')
        if len(password1) < 6:
            messages.error(request,'Passwords too short')
            return render(request , 'registration/password_reset_confirm.html')
        
        user = User.objects.get(username=request.email)
        user.set_password(password1)
        user.is_active = True
        user.save()
        messages.success(request ,'Password changed successfully')
        return render(request , 'registration/password_reset_confirm.html')