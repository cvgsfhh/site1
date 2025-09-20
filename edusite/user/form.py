from django import forms

class UserRegisterForm(forms.Form):
    email = forms.EmailField( widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control '}))


class VerifyEmailForm(forms.Form):
    code = forms.CharField(label='لطفا کد وارد شده به ایمیل را وارد کنید ' ,widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label= 'نام کاربری ',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='رمز عبور '  ,widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class User_loginForm(forms.Form):
    email = forms.EmailField(label='ایمیل',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='رمز عبور ', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class Forget_passwordForm(forms.Form):
    email = forms.EmailField(label='ایمیل ', widget=forms.TextInput(attrs={'class': 'form-control'}))

class User_forgetForm(forms.Form):
    code = forms.CharField(label='لطفا کد وارد شده به ایمیل را وارد کنید ' ,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='یک رمز عبور جدید انتخاب کنید '  ,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    repeat_password = forms.CharField(label='رمز عبور را تکرار کنید '  ,widget=forms.PasswordInput(attrs={'class': 'form-control'}))







