"""
URL configuration for edusite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views_home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from home import views
from product import views as product_views
from user import views as user_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('product/<slug:slug>/',product_views.product,name='product'),
    #__________user______________
    path('register/', user_views.register, name='register'),
    path('verify/',user_views.verify,name='verify'),
    path('login/',user_views.user_login,name='login'),
    path('logout/',user_views.user_logout,name='logout'),
    path('forget_password/',user_views.forget_password,name='forget_password'),
    path('verifyforgetpassword/',user_views.verifyforgetpassword,name='verifyforgetpassword'),
    path('profile/',user_views.profile,name='profile'),
    # __________user______________
]
# user = User.objects.get(id=4)
# user.delete()
#user = User.objects.get('farzad')