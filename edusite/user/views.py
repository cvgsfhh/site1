import random
from django.contrib import messages
from django.contrib.auth.models import User
from urllib3 import request

from product.views import product
from user.form import UserRegisterForm, VerifyEmailForm, User_loginForm, Forget_passwordForm, User_forgetForm
from user.models import Register, Users, Purchases
from django.shortcuts import render, redirect
from utils.utils import send_email, html_body, send_sms
from django.contrib.auth import authenticate, login, logout


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user_phone = form.cleaned_data.get('phone')
            user_email = form.cleaned_data.get('email')
            code = random.randint(1000, 9999)
            reg = Register(user_phone=user_phone, user_email=user_email, code=code)
            reg.save()
            html = html_body(code)
            send_email(user_email, subject='کد فعال سازی آموزشگاه', body=html)
            messages.info(request, 'کد فعال سازی برای شما ایمیل شد')
            return redirect(f"../verify?email={user_email}&phone={user_phone}")
        else:
            messages.error(request, 'ایرادی در فرم وجود دارد')
    elif request.method == "GET":
        if request.user.is_authenticated:
            messages.error(request, 'شما لاگین هستید')
            return redirect("register")
    form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def verify(request):
    if request.method == "POST":
        verify_form = VerifyEmailForm(request.POST)
        if verify_form.is_valid():
            code = verify_form.cleaned_data.get('code')
            email = request.GET.get('email')
            phone = request.GET.get('phone')
            name = verify_form.cleaned_data.get('name')
            password = verify_form.cleaned_data.get('password')
            is_valid_code = Register.objects.filter(code=code, user_email=email).exists()
            if is_valid_code:
                user = Users(user_name=name, user_phone=phone, user_email=email)
                #TODO یوزر بالا دستی ساختیم و یوزر پایین یوزر استاندارد جنگو است
                #TODO نکته یوزر نیم را ایمیل قرار دادیم
                user.save()
                user = User.objects.create_user(email, email, password)
                user.first_name = name
                user.save()
                user = authenticate(request, username=email, password=password)
                login(request, user)

                messages.success(request,'شما با موفقیت ثبت نام شدید')
                Register.objects.filter(user_email=email).delete()

            else:
                messages.error(request, '...کد وارد شده صحیح نیست')
                verify_form = VerifyEmailForm()
        else:
            messages.warning(request, '...اطلاعات وارد شده صحیح نیست')
            verify_form = VerifyEmailForm()

    elif request.method == "GET":
        if request.GET.get("is_sms") == "1":
            messages.info(request, f"کد به {request.GET.get('phone')} ارسال شد")
        elif request.GET.get('phone') is not None:
            messages.info(request, f"کد به {request.GET.get('phone')} ارسال شد")
            verify_form = VerifyEmailForm()
            user_phone = request.GET.get('phone')
            try:
                code = Register.objects.filter(user_phone=user_phone).last().code
                send_sms(user_phone, code)
                print(code)
            except Register.DoesNotExist:
                messages.error(request, "...اطلاعات شما تایید نشد دوباره تلاش کنید")
                send_sms("09302446141", user_phone)  # این خط می‌تواند خطای مربوط به ارسال SMS را مدیریت کند
        else:
            messages.error(request, 'مسیر شما غلط است، از اول شروع کنید')
            return redirect('register')
    verify_form = VerifyEmailForm()
    my_url = f"../verify?email={request.GET.get('email')}&phone={request.GET.get('phone')}"
    return render(request, 'verify.html', {'form': verify_form, 'my_url': my_url})

def user_login(request):
    if request.method == "POST":
        form = User_loginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,'شما با موفقیت وارد شدید')
                return redirect('home')
            else:
                messages.error(request,'نام کاربری یا رمز ورود اشتباه است')
                form = User_loginForm()
    else:
        form = User_loginForm()
    return render(request, template_name='login.html', context={'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'شما با موفقیت از حسابتان خارج شدید')
    return redirect('home')

def forget_password(request):
    if request.method == "POST":
        form = Forget_passwordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            code = random.randint(1000, 9999)
            reg = Register.objects.create(user_email=email, code=code)
            reg.save()
            html = html_body(code)
            send_email(email,'ارسال کد فراموشی',html)
            print(code)
            messages.success(request,'کد فراموشی به ایمیل شما ارسال شد')
            return redirect(f"../verifyforgetpassword?email={email}")
        else:
            messages.error(request,'ایرادی در فرم شما وجود دارد')

    else:
        form = Forget_passwordForm()
    return render(request, template_name='forget_password.html', context={'form': form})

def verifyforgetpassword(request):
    if request.method == "POST":
        form = User_forgetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            code = form.cleaned_data.get('code')
            repeat_password = form.cleaned_data.get('repeat_password')
            if password==repeat_password:
                reg = Register.objects.filter(code=code ,user_email=request.GET.get('email'))
                if reg.exists():
                    user = User.objects.get(email=request.GET.get('email'))
                    user.set_password(password)
                    user.save()
                    reg.delete()
                    messages.success(request,'رمز عبور شما با موفقیت تغییر کرد')
                else:
                    messages.error(request,'کد وارد شده صحیح نیست')
            else:
                messages.error(request,'رمز عبور یکسان نیست')
        else:
            messages.error(request,'ایرادی در فرم وجود دارد')
    else:
      form = User_forgetForm()
    return render(request, template_name='verify-forget-pass.html', context={'form': form})

def profile(request):

    email = request.user.email
    #todo لیست خرید کاربر با ایمیل خودش رو نمایش میدیم
    user = Users.objects.get(user_email=email)
    purchases = Purchases.objects.get(user=user)
    products = purchases.product



    return render(request,'profile.html',{"products":products})