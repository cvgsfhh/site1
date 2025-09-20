
from django.db import models
from django.contrib.auth.models import AbstractUser

# مدل اصلی کاربر که جایگزین مدل پیش‌فرض جنگو می‌شود
class CustomUser(AbstractUser):
    # ما ایمیل را به عنوان نام کاربری اصلی در نظر می‌گیریم
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name='شماره تلفن')
    
    # این فیلدها را از مدل پیش‌فرض جنگو داریم، فقط نام نمایشی آنها را فارسی می‌کنیم
    first_name = models.CharField(max_length=150, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='نام خانوادگی')

    # مشخص می‌کنیم که برای لاگین از فیلد ایمیل استفاده شود
    USERNAME_FIELD = 'email'
    # فیلدهای ضروری هنگام ساخت سوپریوزر را مشخص می‌کنیم (ایمیل از قبل در USERNAME_FIELD است)
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# مدل موقت برای نگهداری کد تایید ثبت‌نام
class RegistrationProfile(models.Model):
    email = models.EmailField(verbose_name='ایمیل')
    phone_number = models.CharField(max_length=15, verbose_name='شماره تلفن')
    name = models.CharField(max_length=150, verbose_name='نام')
    password = models.CharField(max_length=128, verbose_name='رمز عبور (هش شده)') # مهم: رمز عبور باید هش شود
    verification_code = models.CharField(max_length=6, verbose_name='کد تایید')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')

    def __str__(self):
        return f"Profile for {self.email}"

# مدل برای نگهداری خریدهای کاربر
class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='purchases', verbose_name='کاربر')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, verbose_name='محصول') # فرض شده اپ محصول دارید
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ خرید')

    def __str__(self):
        return f"{self.user.email} bought {self.product.name}"

