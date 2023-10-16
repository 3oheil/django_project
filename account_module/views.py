from django.shortcuts import render, redirect
from django.views import View
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.http import Http404, HttpRequest
from django.contrib.auth import login, logout
from utils.send_email import send_email

from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from .models import User


# Create your views here.


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        print(get_random_string(72))
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register_page.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'ایمیل وارد شده تکراری می باشد')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=True,
                    username=user_email)
                new_user.set_password(user_password)
                new_user.save()

                return redirect(reverse('login_page'))

                # send_email('فعالسازی حساب کاربری', )

                # todo: send email active code for user

        context = {
            'register_form': register_form
        }

        return render(request, 'account_module/register_page.html', context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login_page.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('email', 'نام کاربری یا رمز عبور اشتباه است ')
            else:
                login_form.add_error('email', 'کاربری با ایمیل وارد شده یافت نشد')

        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/register_page.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # todo : show success message for user
                return redirect(reverse('login_page'))
            else:
                pass
                # todo: show your account was activated for user
        raise Http404


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_password = ForgetPasswordForm()
        context = {
            'forget_password': forget_password
        }
        return render(request, 'account_module/forget_password_page.html', context)

    def post(self, request: HttpRequest):
        forget_password = ForgetPasswordForm(request.POST)
        if forget_password.is_valid():
            user_email = forget_password.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                # todo : send email active code to user
                pass
            context = {
                'forget_password': forget_password
            }
            return render(request, 'account_module/forget_password_page.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))

        reset_password = ResetPasswordForm()
        context = {
            'reset_password': reset_password,
            'user': user
        }
        return render(request, 'account_module/reset_password_page.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_password = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_password.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            new_user_password = reset_password.cleaned_data.get('password')
            user.set_password(new_user_password)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_password': reset_password,
            'user': user
        }
        return render(request, 'account_module/reset_password_page.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))