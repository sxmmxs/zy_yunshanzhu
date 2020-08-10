from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'users$', views.UserView.as_view(), name='user')
]
