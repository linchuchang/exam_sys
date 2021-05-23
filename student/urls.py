from django.conf.urls import url
from student import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.index),
    path('/log', views.student_login, name='log')
]