"""djangoProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from student import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index, name='index'),
    # 注册的url
    path('register_s/', views.register, name='register_s'),
    path('register_t/', views.register_t, name='register_t'),
    # 登录的url
    path('login/', views.student_login, name='login'),
    # 计算成绩的url
    path('calGrade/', views.calGrade),
    path('upload/', views.upload_file, name='upload'),
    url(r'^student', include('student.urls')),
    path('exam/', views.exam),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('logout/', views.logout, name='logout'),
    # 验证码发送
    path('register_s/verify/', views.verify, name="verify"),
    # 配置试卷
    path('makepaper/', views.makepaper, name="makepaper"),
    path('create_paper/', views.create_Paper, name="create_paper"),
]
